from collections import Mapping
from typing import Mapping as MappingType
from jsons.deserializers import default_dict_deserializer


def default_mapping_deserializer(obj: Mapping, cls: type, **kwargs) -> Mapping:
    """
    Deserialize a (JSON) list into a set by deserializing all items of that
    list. If the list as a generic type (e.g. Set[datetime]) then it is
    assumed that all elements can be deserialized to that type.
    :param obj: the list that needs deserializing.
    :param cls: the type, optionally with a generic (e.g. Set[str]).
    :param kwargs: any keyword arguments.
    :return: a deserialized set instance.
    """
    cls_ = Mapping
    if hasattr(cls, '__args__'):
        cls_ = MappingType[cls.__args__]
    dict_ = default_dict_deserializer(obj, cls_, **kwargs)
    result = dict_
    # Strip any generics from cls to allow for an instance check.
    stripped_cls = getattr(cls, '__extra__', cls)
    if not isinstance(result, stripped_cls):
        result = cls(dict_)
    return result
