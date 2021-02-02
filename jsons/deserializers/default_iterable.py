from collections.abc import Mapping, Iterable
from typing import Iterable as IterableType

from jsons._compatibility_impl import get_naked_class
from jsons.deserializers.default_list import default_list_deserializer


def default_iterable_deserializer(
        obj: list,
        cls: type,
        **kwargs) -> Iterable:
    """
    Deserialize a (JSON) list into an ``Iterable`` by deserializing all items
    of that list. The given obj is assumed to be homogeneous; if the list has a
    generic type (e.g. Set[datetime]) then it is assumed that all elements can
    be deserialized to that type.
    :param obj: The list that needs deserializing to an ``Iterable``.
    :param cls: The type, optionally with a generic (e.g. Deque[str]).
    :param kwargs: Any keyword arguments.
    :return: A deserialized ``Iterable`` (e.g. ``set``) instance.
    """
    cls_ = Mapping
    if hasattr(cls, '__args__'):
        cls_ = IterableType[cls.__args__]
    list_ = default_list_deserializer(obj, cls_, **kwargs)
    result = list_
    naked_cls = get_naked_class(cls)
    if not isinstance(result, naked_cls):
        result = naked_cls(list_)
    return result
