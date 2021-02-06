"""
PRIVATE MODULE: do not import (from) it directly.

This module contains implementations of common functionality that can be used
throughout `jsons`.
"""
import builtins
import warnings
from importlib import import_module
from typing import Callable, Optional, Tuple, TypeVar, Any

from jsons._cache import cached
from jsons._compatibility_impl import get_union_params
from jsons.exceptions import UnknownClassError

NoneType = type(None)
JSON_KEYS = (str, int, float, bool, NoneType)
VALID_TYPES = (str, int, float, bool, list, tuple, set, dict, NoneType)
META_ATTR = '-meta'  # The name of the attribute holding meta info.
T = TypeVar('T')


class StateHolder:
    """
    This class holds the registered serializers and deserializers.
    """
    _fork_counter = 0
    _classes_serializers = list()
    _classes_deserializers = list()
    _serializers = dict()
    _deserializers = dict()
    _validators = dict()
    _classes_validators = list()
    _announced_classes = dict()
    _suppress_warnings = False
    _suppressed_warnings = set()

    @classmethod
    def _warn(cls, msg, code, *args, **kwargs):
        if not cls._suppress_warnings and code not in cls._suppressed_warnings:
            msg_ = ('{} Use suppress_warning({}) or suppress_warnings(True) to '
                    'turn off this message.'.format(msg, code))
            warnings.warn(msg_, *args, **kwargs)


@cached
def get_class_name(cls: type,
                   transformer: Optional[Callable[[str], str]] = None,
                   fully_qualified: bool = False) -> Optional[str]:
    """
    Return the name of a class.
    :param cls: the class of which the name if to be returned.
    :param transformer: any string transformer, e.g. ``str.lower``.
    :param fully_qualified: if ``True`` return the fully qualified name (i.e.
    complete with module name).
    :return: the name of ``cls``, transformed if a transformer is given.
    """
    transformer = transformer or (lambda x: x)
    cls_name = _get_special_cases(cls)
    if cls_name:
        return transformer(cls_name)
    cls_name = _get_simple_name(cls)
    if fully_qualified:
        module = _get_module(cls)
        if module:
            cls_name = '{}.{}'.format(module, cls_name)
    cls_name = transformer(cls_name)
    return cls_name


def _get_special_cases(cls: type):
    if (hasattr(cls, '__qualname__')
            and cls.__qualname__ == 'NewType.<locals>.new_type'):
        return cls.__name__


def get_cls_from_str(cls_str: str, source: object, fork_inst) -> type:
    cls = getattr(builtins, cls_str, None)
    if cls:
        return cls
    if '[' in cls_str and ']' in cls_str:
        return _get_generic_cls_from_str(cls_str, source, fork_inst)
    try:
        splitted = cls_str.split('.')
        module_name = '.'.join(splitted[:-1])
        cls_name = splitted[-1]
        cls_module = import_module(module_name)
        cls = getattr(cls_module, cls_name)
    except (ImportError, AttributeError, ValueError):
        cls = _lookup_announced_class(cls_str, source, fork_inst)
    return cls


def _get_generic_cls_from_str(cls_str: str, source: object, fork_inst) -> type:
    # If cls_str represents a generic type, try to parse the sub types.
    origin_str, subtypes_str = cls_str.split('[')
    subtypes_str = subtypes_str[0:-1]  # Remove the ']'.
    origin = get_cls_from_str(origin_str, source, fork_inst)
    subtypes = [get_cls_from_str(s.strip(), source, fork_inst)
                for s in subtypes_str.split(',')]
    return origin[tuple(subtypes)]


def determine_precedence(
        cls: type,
        cls_from_meta: type,
        cls_from_type: type,
        inferred_cls: bool):
    order = [cls, cls_from_meta, cls_from_type]
    if inferred_cls:
        # The type from a verbose dumped object takes precedence over an
        # inferred type (e.g. T in List[T]).
        order = [cls_from_meta, cls, cls_from_type]
    # Now to return the first element in the order that holds a value.
    for elem in order:
        if elem:
            return elem


def get_cls_and_meta(
        json_obj: object,
        fork_inst: type) -> Tuple[Optional[type], Optional[dict]]:
    if isinstance(json_obj, dict) and META_ATTR in json_obj:
        cls_str = json_obj[META_ATTR]['classes']['/']
        cls = get_cls_from_str(cls_str, json_obj, fork_inst)
        return cls, json_obj[META_ATTR]
    return None, None


def can_match_with_none(cls: type):
    # Return True if cls allows None; None is a valid value with the given cls.
    result = cls in (Any, object, None, NoneType)
    if not result:
        cls_name = get_class_name(cls).lower()
        result = (('union' in cls_name or 'optional' in cls_name)
                  and NoneType in get_union_params(cls))
    return result


def _lookup_announced_class(
        cls_str: str,
        source: object,
        fork_inst: type) -> type:
    cls = fork_inst._announced_classes.get(cls_str)
    if not cls:
        msg = ('Could not find a suitable type for "{}". Make sure it can be '
               'imported or that is has been announced.'.format(cls_str))
        raise UnknownClassError(msg, source, cls_str)
    return cls


def _get_simple_name(cls: type) -> str:
    if cls is None:
        cls = type(cls)
    cls_name = getattr(cls, '__name__', None)
    if not cls_name:
        cls_name = getattr(cls, '_name', None)
    if not cls_name:
        cls_name = repr(cls)
        cls_name = cls_name.split('[')[0]  # Remove generic types.
        cls_name = cls_name.split('.')[-1]  # Remove any . caused by repr.
        cls_name = cls_name.split(r"'>")[0]  # Remove any '>.
    return cls_name


def _get_module(cls: type) -> Optional[str]:
    builtin_module = str.__class__.__module__
    module = getattr(cls, '__module__', None)
    if module and module != builtin_module:
        return module
