from collections import deque
from typing import Deque
from jsons.deserializers import default_list_deserializer


def default_deque_deserializer(obj: list, cls: type = None, **kwargs) -> deque:
    """
    Deserialize a deque by deserializing all items of that deque.
    :param obj: the list that needs deserializing.
    :param cls: the type optionally with a generic (e.g. Deque[str]).
    :param kwargs: any keyword arguments.
    :return: a deserialized deque instance.
    """
    cls_ = list
    if hasattr(cls, '__args__'):
        cls_ = Deque[cls.__args__[0]]
    list_ = default_list_deserializer(obj, cls_, **kwargs)
    return deque(list_)
