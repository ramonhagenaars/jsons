"""
PRIVATE MODULE: do not import (from) it directly.

This module contains functionality for dumping stuff to json.
"""
import json
from typing import Optional, Dict

from jsons._cache import clear
from jsons._common_impl import StateHolder
from jsons._extra_impl import announce_class
from jsons._lizers_impl import get_serializer
from jsons.exceptions import SerializationError


def dump(obj: object,
         cls: Optional[type] = None,
         *,
         strict: bool = False,
         fork_inst: Optional[type] = StateHolder,
         **kwargs) -> object:
    """
    Serialize the given ``obj`` to a JSON equivalent type (e.g. dict, list,
    int, ...).

    The way objects are serialized can be finetuned by setting serializer
    functions for the specific type using ``set_serializer``.

    You can also provide ``cls`` to specify that ``obj`` needs to be serialized
    as if it was of type ``cls`` (meaning to only take into account attributes
    from ``cls``). The type ``cls`` must have a ``__slots__`` defined. Any type
    will do, but in most cases you may want ``cls`` to be a base class of
    ``obj``.
    :param obj: a Python instance of any sort.
    :param cls: if given, ``obj`` will be dumped as if it is of type ``type``.
    :param strict: a bool to determine if the serializer should be strict
    (i.e. only dumping stuff that is known to ``cls``).
    :param fork_inst: if given, it uses this fork of ``JsonSerializable``.
    :param kwargs: the keyword args are passed on to the serializer function.
    :return: the serialized obj as a JSON type.
    """
    cls_ = cls or obj.__class__
    serializer = get_serializer(cls_, fork_inst)

    # Is this the initial call or a nested?
    initial = kwargs.get('_initial', True)

    kwargs_ = {
        'fork_inst': fork_inst,
        '_initial': False,
        'strict': strict,
        **kwargs
    }
    announce_class(cls_, fork_inst=fork_inst)
    # kwargs['_objects'].remove(id(obj))
    return _do_dump(obj, serializer, cls, initial, kwargs_)


def _do_dump(obj, serializer, cls, initial, kwargs):
    try:
        result = serializer(obj, cls=cls, **kwargs)
        if initial:
            clear()
        return result
    except Exception as err:
        clear()
        raise SerializationError(str(err)) from err


def dumps(obj: object,
          jdkwargs: Optional[Dict[str, object]] = None,
          *args,
          **kwargs) -> str:
    """
    Extend ``json.dumps``, allowing any Python instance to be dumped to a
    string. Any extra (keyword) arguments are passed on to ``json.dumps``.

    :param obj: the object that is to be dumped to a string.
    :param jdkwargs: extra keyword arguments for ``json.dumps`` (not
    ``jsons.dumps``!)
    :param args: extra arguments for ``jsons.dumps``.
    :param kwargs: Keyword arguments that are passed on through the
    serialization process.
    passed on to the serializer function.
    :return: ``obj`` as a ``str``.
    """
    jdkwargs = jdkwargs or {}
    dumped = dump(obj, *args, **kwargs)
    return json.dumps(dumped, **jdkwargs)


def dumpb(obj: object,
          encoding: str = 'utf-8',
          jdkwargs: Optional[Dict[str, object]] = None,
          *args,
          **kwargs) -> bytes:
    """
    Extend ``json.dumps``, allowing any Python instance to be dumped to bytes.
    Any extra (keyword) arguments are passed on to ``json.dumps``.

    :param obj: the object that is to be dumped to bytes.
    :param encoding: the encoding that is used to transform to bytes.
    :param jdkwargs: extra keyword arguments for ``json.dumps`` (not
    ``jsons.dumps``!)
    :param args: extra arguments for ``jsons.dumps``.
    :param kwargs: Keyword arguments that are passed on through the
    serialization process.
    passed on to the serializer function.
    :return: ``obj`` as ``bytes``.
    """
    jdkwargs = jdkwargs or {}
    dumped_dict = dump(obj, *args, **kwargs)
    dumped_str = json.dumps(dumped_dict, **jdkwargs)
    return dumped_str.encode(encoding=encoding)
