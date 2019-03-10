"""
PRIVATE MODULE: do not import (from) it directly.

This module contains implementations of common functionality that can be used
throughout `jsons`.
"""
from typing import Callable, Optional


META_ATTR = '-meta'  # The name of the attribute holding meta info.


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
    cls_name = getattr(cls, '__name__', getattr(cls, '_name', None))
    module = _get_module(cls)
    transformer = transformer or (lambda x: x)
    if not cls_name and hasattr(cls, '__origin__'):
        origin = cls.__origin__
        cls_name = get_class_name(origin)
    if not cls_name:
        cls_name = str(cls)
    if fully_qualified and module:
        cls_name = '{}.{}'.format(module, cls_name)
    cls_name = transformer(cls_name)
    return cls_name


def _get_module(cls: type) -> Optional[str]:
    builtin_module = str.__class__.__module__
    module = cls.__module__
    if module and module != builtin_module:
        return module


def get_parents(cls: type, lizers: list) -> list:
    """
    Return a list of serializers or deserializers that can handle a parent
    of ``cls``.
    :param cls: the type that
    :param lizers: a list of serializers or deserializers.
    :return: a list of serializers or deserializers.
    """
    parents = []
    for cls_ in lizers:
        try:
            if issubclass(cls, cls_):
                parents.append(cls_)
        except TypeError:
            pass  # Some types do not support `issubclass` (e.g. Union).
    return parents
