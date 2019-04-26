"""
PRIVATE MODULE: do not import (from) it directly.

This module contains implementations of common functionality that can be used
throughout `jsons`.
"""
import builtins
import warnings
from importlib import import_module
from typing import Callable, Optional, Tuple
from jsons.exceptions import UnknownClassError


VALID_TYPES = (str, int, float, bool, list, tuple, set, dict, type(None))
META_ATTR = '-meta'  # The name of the attribute holding meta info.


class StateHolder:
    """
    This class holds the registered serializers and deserializers.
    """
    _classes_serializers = list()
    _classes_deserializers = list()
    _serializers = dict()
    _deserializers = dict()
    _announced_classes = dict()
    _suppress_warnings = False

    @classmethod
    def _warn(cls, msg, *args, **kwargs):
        if not cls._suppress_warnings:
            msg_ = ('{} You can suppress warnings like this using '
                    'jsons.suppress_warnings().'.format(msg))
            warnings.warn(msg_, *args, **kwargs)


def get_class_name(cls: type,
                   transformer: Optional[Callable[[str], str]] = None,
                   fully_qualified: bool = False,
                   fork_inst: Optional[type] = StateHolder) -> Optional[str]:
    """
    Return the name of a class.
    :param cls: the class of which the name if to be returned.
    :param transformer: any string transformer, e.g. ``str.lower``.
    :param fully_qualified: if ``True`` return the fully qualified name (i.e.
    complete with module name).
    :param fork_inst if given, it uses this fork of ``JsonSerializable`` for
    finding the class name.
    :return: the name of ``cls``, transformed if a transformer is given.
    """

    transformer = transformer or (lambda x: x)
    cls_name = _get_special_cases(cls)
    if cls_name:
        return transformer(cls_name)
    if cls in fork_inst._announced_classes:
        return transformer(fork_inst._announced_classes[cls])
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
    try:
        splitted = cls_str.split('.')
        module_name = '.'.join(splitted[:-1])
        cls_name = splitted[-1]
        cls_module = import_module(module_name)
        cls = getattr(cls_module, cls_name)
    except (ImportError, AttributeError, ValueError):
        cls = _lookup_announced_class(cls_str, source, fork_inst)
    return cls


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
    module = cls.__module__
    if module and module != builtin_module:
        return module
