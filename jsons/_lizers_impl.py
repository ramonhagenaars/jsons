"""
PRIVATE MODULE: do not import (from) it directly.

This module contains functionality for setting and getting serializers and
deserializers.
"""
from typing import Optional, Dict, Sequence, Union

from jsons._cache import cached
from jsons._common_impl import StateHolder, get_class_name
from jsons._compatibility_impl import get_naked_class


def set_serializer(
        func: callable,
        cls: Union[type, Sequence[type]],
        high_prio: bool = True,
        fork_inst: type = StateHolder) -> None:
    """
    Set a serializer function for the given type. You may override the default
    behavior of ``jsons.load`` by setting a custom serializer.

    The ``func`` argument must take one argument (i.e. the object that is to be
    serialized) and also a ``kwargs`` parameter. For example:

    >>> def func(obj, **kwargs):
    ...    return dict()

    You may ask additional arguments between ``cls`` and ``kwargs``.

    :param func: the serializer function.
    :param cls: the type or sequence of types this serializer can handle.
    :param high_prio: determines the order in which is looked for the callable.
    :param fork_inst: if given, it uses this fork of ``JsonSerializable``.
    :return: None.
    """
    if isinstance(cls, Sequence):
        for cls_ in cls:
            set_serializer(func, cls_, high_prio, fork_inst)
    elif cls:
        index = 0 if high_prio else len(fork_inst._classes_serializers)
        fork_inst._classes_serializers.insert(index, cls)
        cls_name = get_class_name(cls, fully_qualified=True)
        fork_inst._serializers[cls_name.lower()] = func
    else:
        fork_inst._serializers['nonetype'] = func


def set_deserializer(
        func: callable,
        cls: Union[type, Sequence[type]],
        high_prio: bool = True,
        fork_inst: type = StateHolder) -> None:
    """
    Set a deserializer function for the given type. You may override the
    default behavior of ``jsons.dump`` by setting a custom deserializer.

    The ``func`` argument must take two arguments (i.e. the dict containing the
    serialized values and the type that the values should be deserialized into)
    and also a ``kwargs`` parameter. For example:

    >>> def func(dict_, cls, **kwargs):
    ...    return cls()

    You may ask additional arguments between ``cls`` and ``kwargs``.

    :param func: the deserializer function.
    :param cls: the type or sequence of types this serializer can handle.
    :param high_prio: determines the order in which is looked for the callable.
    :param fork_inst: if given, it uses this fork of ``JsonSerializable``.
    :return: None.
    """
    if isinstance(cls, Sequence):
        for cls_ in cls:
            set_deserializer(func, cls_, high_prio, fork_inst)
    elif cls:
        index = 0 if high_prio else len(fork_inst._classes_deserializers)
        fork_inst._classes_deserializers.insert(index, cls)
        cls_name = get_class_name(cls, fully_qualified=True)
        fork_inst._deserializers[cls_name.lower()] = func
    else:
        fork_inst._deserializers['nonetype'] = func


@cached
def get_serializer(
        cls: type,
        fork_inst: Optional[type] = StateHolder) -> callable:
    """
    Return the serializer function that would be used for the given ``cls``.
    :param cls: the type for which a serializer is to be returned.
    :param fork_inst: if given, it uses this fork of ``JsonSerializable``.
    :return: a serializer function.
    """
    serializer = _get_lizer(cls, fork_inst._serializers,
                            fork_inst._classes_serializers, fork_inst)
    return serializer


@cached
def get_deserializer(
        cls: type,
        fork_inst: Optional[type] = StateHolder) -> callable:
    """
    Return the deserializer function that would be used for the given ``cls``.
    :param cls: the type for which a deserializer is to be returned.
    :param fork_inst: if given, it uses this fork of ``JsonSerializable``.
    :return: a deserializer function.
    """
    deserializer = _get_lizer(cls, fork_inst._deserializers,
                              fork_inst._classes_deserializers, fork_inst)
    return deserializer


def _get_lizer(
        cls: type,
        lizers: Dict[str, callable],
        classes_lizers: list,
        fork_inst: type,
        recursive: bool = False) -> callable:
    cls_name = get_class_name(cls, str.lower, fully_qualified=True)
    lizer = (lizers.get(cls_name, None)
             or _get_lizer_by_parents(cls, lizers, classes_lizers, fork_inst))
    if not lizer and not recursive and hasattr(cls, '__supertype__'):
        return _get_lizer(cls.__supertype__, lizers,
                          classes_lizers, fork_inst, True)
    return lizer


def _get_lizer_by_parents(
        cls: type,
        lizers: Dict[str, callable],
        classes_lizers: list,
        fork_inst: type) -> callable:
    result = None
    parents = _get_parents(cls, classes_lizers)
    if parents:
        pname = get_class_name(parents[0], str.lower, fully_qualified=True)
        result = lizers[pname]
    return result


def _get_parents(cls: type, lizers: list) -> list:
    """
    Return a list of serializers or deserializers that can handle a parent
    of ``cls``.
    :param cls: the type that
    :param lizers: a list of serializers or deserializers.
    :return: a list of serializers or deserializers.
    """
    parents = []
    naked_cls = get_naked_class(cls)
    for cls_ in lizers:
        try:
            if issubclass(naked_cls, cls_):
                parents.append(cls_)
        except (TypeError, AttributeError):
            pass  # Some types do not support `issubclass` (e.g. Union).
    return parents
