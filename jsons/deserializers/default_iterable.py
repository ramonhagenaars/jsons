from collections import Mapping, Iterable
from typing import Iterable as IterableType
from jsons.deserializers import default_list_deserializer


def default_iterable_deserializer(
        obj: Iterable,
        cls: type,
        **kwargs) -> Iterable:
    """
    Deserialize a (JSON) list into an ``Iterable`` by deserializing all items
    of that list. The given obj is assumed to be homogeneous; if the list has a
    generic type (e.g. Set[datetime]) then it is assumed that all elements can
    be deserialized to that type.
    :param obj: the list that needs deserializing.
    :param cls: the type, optionally with a generic (e.g. Deque[str]).
    :param kwargs: any keyword arguments.
    :return: a deserialized ``Iterable`` (e.g. ``set``) instance.
    """
    cls_ = Mapping
    if hasattr(cls, '__args__'):
        cls_ = IterableType[cls.__args__]
    list_ = default_list_deserializer(obj, cls_, **kwargs)
    result = list_
    # Strip any generics from cls to allow for an instance check.
    stripped_cls = getattr(cls, '__extra__', cls)
    if not isinstance(result, stripped_cls):
        result = stripped_cls(list_)
    return result
