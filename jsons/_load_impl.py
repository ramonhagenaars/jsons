"""
PRIVATE MODULE: do not import (from) it directly.

This module contains functionality for loading stuff from json.
"""
import json
from json import JSONDecodeError
from typing import Optional, Dict, Callable, Tuple, Any, Type

from jsons._cache import clear
from jsons._common_impl import (
    StateHolder,
    get_cls_from_str,
    get_class_name,
    get_cls_and_meta,
    determine_precedence,
    VALID_TYPES,
    T,
    can_match_with_none
)
from jsons._lizers_impl import get_deserializer
from jsons._validation import validate
from jsons.exceptions import DeserializationError, JsonsError, DecodeError


def load(
        json_obj: object,
        cls: Optional[Type[T]] = None,
        *,
        strict: bool = False,
        fork_inst: Optional[type] = StateHolder,
        attr_getters: Optional[Dict[str, Callable[[], object]]] = None,
        **kwargs) -> T:
    """
    Deserialize the given ``json_obj`` to an object of type ``cls``. If the
    contents of ``json_obj`` do not match the interface of ``cls``, a
    DeserializationError is raised.

    If ``json_obj`` contains a value that belongs to a custom class, there must
    be a type hint present for that value in ``cls`` to let this function know
    what type it should deserialize that value to.


    **Example**:

    >>> from typing import List
    >>> import jsons
    >>> class Person:
    ...     # No type hint required for name
    ...     def __init__(self, name):
    ...         self.name = name
    >>> class Family:
    ...     # Person is a custom class, use a type hint
    ...         def __init__(self, persons: List[Person]):
    ...             self.persons = persons
    >>> loaded = jsons.load({'persons': [{'name': 'John'}]}, Family)
    >>> loaded.persons[0].name
    'John'

    If no ``cls`` is given, a dict is simply returned, but contained values
    (e.g. serialized ``datetime`` values) are still deserialized.

    If `strict` mode is off and the type of `json_obj` exactly matches `cls`
    then `json_obj` is simply returned.

    :param json_obj: the dict that is to be deserialized.
    :param cls: a matching class of which an instance should be returned.
    :param strict: a bool to determine if the deserializer should be strict
    (i.e. fail on a partially deserialized `json_obj` or on `None`).
    :param fork_inst: if given, it uses this fork of ``JsonSerializable``.
    :param attr_getters: a ``dict`` that may hold callables that return values
    for certain attributes.
    :param kwargs: the keyword args are passed on to the deserializer function.
    :return: an instance of ``cls`` if given, a dict otherwise.
    """
    _check_for_none(json_obj, cls)
    if _should_skip(json_obj, cls, strict):
        validate(json_obj, cls, fork_inst)
        return json_obj
    if isinstance(cls, str):
        cls = get_cls_from_str(cls, json_obj, fork_inst)
    original_cls = cls
    cls, meta_hints = _check_and_get_cls_and_meta_hints(
        json_obj, cls, fork_inst, kwargs.get('_inferred_cls', False))

    deserializer = get_deserializer(cls, fork_inst)

    # Is this the initial call or a nested?
    initial = kwargs.get('_initial', True)

    kwargs_ = {
        'meta_hints': meta_hints,  # Overridable by kwargs.
        **kwargs,
        'strict': strict,
        'fork_inst': fork_inst,
        'attr_getters': attr_getters,
        '_initial': False,
        '_inferred_cls': cls is not original_cls,
    }

    return _do_load(json_obj, deserializer, cls, initial, **kwargs_)


def _do_load(json_obj: object,
             deserializer: callable,
             cls: type,
             initial: bool,
             **kwargs):
    cls_name = get_class_name(cls, fully_qualified=True)
    if deserializer is None:
        raise DeserializationError('No deserializer for type "{}"'.format(cls_name), json_obj, cls)
    try:
        result = deserializer(json_obj, cls, **kwargs)
        validate(result, cls, kwargs['fork_inst'])
    except Exception as err:
        clear()
        if isinstance(err, JsonsError):
            raise
        message = 'Could not deserialize value "{}" into "{}". {}'.format(json_obj, cls_name, err)
        raise DeserializationError(message, json_obj, cls) from err
    else:
        if initial:
            # Clear all lru caches right before returning the initial call.
            clear()
        return result


def loads(
        str_: str,
        cls: Optional[Type[T]] = None,
        jdkwargs: Optional[Dict[str, object]] = None,
        *args,
        **kwargs) -> T:
    """
    Extend ``json.loads``, allowing a string to be loaded into a dict or a
    Python instance of type ``cls``. Any extra (keyword) arguments are passed
    on to ``json.loads``.

    :param str_: the string that is to be loaded.
    :param cls: a matching class of which an instance should be returned.
    :param jdkwargs: extra keyword arguments for ``json.loads`` (not
    ``jsons.loads``!)
    :param args: extra arguments for ``jsons.loads``.
    :param kwargs: extra keyword arguments for ``jsons.loads``.
    :return: a JSON-type object (dict, str, list, etc.) or an instance of type
    ``cls`` if given.
    """
    jdkwargs = jdkwargs or {}
    try:
        obj = json.loads(str_, **jdkwargs)
    except JSONDecodeError as err:
        raise DecodeError('Could not load a dict; the given string is not '
                          'valid JSON.', str_, cls, err) from err
    else:
        return load(obj, cls, *args, **kwargs)


def loadb(
        bytes_: bytes,
        cls: Optional[Type[T]] = None,
        encoding: str = 'utf-8',
        jdkwargs: Optional[Dict[str, object]] = None,
        *args,
        **kwargs) -> T:
    """
    Extend ``json.loads``, allowing bytes to be loaded into a dict or a Python
    instance of type ``cls``. Any extra (keyword) arguments are passed on to
    ``json.loads``.

    :param bytes_: the bytes that are to be loaded.
    :param cls: a matching class of which an instance should be returned.
    :param encoding: the encoding that is used to transform from bytes.
    :param jdkwargs: extra keyword arguments for ``json.loads`` (not
    ``jsons.loads``!)
    :param args: extra arguments for ``jsons.loads``.
    :param kwargs: extra keyword arguments for ``jsons.loads``.
    :return: a JSON-type object (dict, str, list, etc.) or an instance of type
    ``cls`` if given.
    """
    if not isinstance(bytes_, bytes):
        raise DeserializationError('loadb accepts bytes only, "{}" was given'
                                   .format(type(bytes_)), bytes_, cls)
    jdkwargs = jdkwargs or {}
    str_ = bytes_.decode(encoding=encoding)
    return loads(str_, cls, jdkwargs=jdkwargs, *args, **kwargs)


def _check_and_get_cls_and_meta_hints(
        json_obj: object,
        cls: type,
        fork_inst: type,
        inferred_cls: bool) -> Tuple[type, Optional[dict]]:
    # Check if json_obj is of a valid type and return the cls.
    if type(json_obj) not in VALID_TYPES:
        invalid_type = get_class_name(type(json_obj), fully_qualified=True)
        valid_types = [get_class_name(typ, fully_qualified=True)
                       for typ in VALID_TYPES]
        msg = ('Invalid type: "{}", only arguments of the following types are '
               'allowed: {}'.format(invalid_type, ", ".join(valid_types)))
        raise DeserializationError(msg, json_obj, cls)

    cls_from_meta, meta = get_cls_and_meta(json_obj, fork_inst)
    meta_hints = meta.get('classes', {}) if meta else {}
    return determine_precedence(
        cls, cls_from_meta, type(json_obj), inferred_cls), meta_hints


def _should_skip(json_obj: object, cls: type, strict: bool):
    return (not strict and type(json_obj) == cls) or cls is Any


def _check_for_none(json_obj: object, cls: type):
    # Check if the json_obj is None and whether or not that is fine.
    if json_obj is None and not can_match_with_none(cls):
        cls_name = get_class_name(cls)
        raise DeserializationError(
            message='NoneType cannot be deserialized into {}'.format(cls_name),
            source=json_obj,
            target=cls)
