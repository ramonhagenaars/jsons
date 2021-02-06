from collections.abc import Mapping
from typing import Mapping as MappingType

from typish import get_args, get_origin

from jsons.deserializers.default_dict import default_dict_deserializer


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
    cls_args = get_args(cls)
    if cls_args:
        cls_ = MappingType[cls_args]
    dict_ = default_dict_deserializer(obj, cls_, **kwargs)
    result = dict_
    # Strip any generics from cls to allow for an instance check.
    if not isinstance(result, get_origin(cls)):
        result = cls(dict_)
    return result
