from collections.abc import Mapping
from typing import Mapping as MappingType
from jsons._common_impl import get_naked_class
from jsons.deserializers import default_dict_deserializer


def default_mapping_deserializer(obj: dict, cls: type, **kwargs) -> Mapping:
    """
    Deserialize a (JSON) dict into a mapping by deserializing all items of that
    dict.
    :param obj: the dict that needs deserializing.
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
    naked_cls = get_naked_class(cls)
    if not isinstance(result, naked_cls):
        result = cls(dict_)
    return result
