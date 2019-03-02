from typing import List
from jsons.deserializers import default_list_deserializer


def default_set_deserializer(obj: list, cls: type, **kwargs) -> set:
    """
    Deserialize a (JSON) list into a set by deserializing all items of that
    list. If the list as a generic type (e.g. Set[datetime]) then it is
    assumed that all elements can be deserialized to that type.
    :param obj: the list that needs deserializing.
    :param cls: the type, optionally with a generic (e.g. Set[str]).
    :param kwargs: any keyword arguments.
    :return: a deserialized set instance.
    """
    cls_ = list
    if hasattr(cls, '__args__'):
        cls_ = List[cls.__args__[0]]
    list_ = default_list_deserializer(obj, cls_, **kwargs)
    return set(list_)
