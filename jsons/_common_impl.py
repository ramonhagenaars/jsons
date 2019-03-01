"""
PRIVATE MODULE: do not import (from) it directly.

This module contains implementations of common functionality that can be used
throughout `jsons`.
"""
from typing import Callable, Optional


def get_class_name(cls: type,
                   transformer: Optional[Callable[[str], str]] = None) \
        -> Optional[str]:
    """
    Return the name of a class.
    :param cls: the class of which the name if to be returned.
    :param transformer: any string transformer, e.g. ``str.lower``.
    :return: the name of ``cls``, transformed if a transformer is given.
    """
    cls_name = getattr(cls, '__name__', getattr(cls, '_name', None))
    if not cls_name and hasattr(cls, '__origin__'):
        origin = cls.__origin__
        cls_name = get_class_name(origin)
    if not cls_name:
        cls_name = str(cls)
    if cls_name and transformer:
        cls_name = transformer(cls_name)
    return cls_name


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
