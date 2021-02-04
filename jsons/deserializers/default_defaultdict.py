from collections import defaultdict
from typing import Optional, Callable, Dict

from typish import get_args

from jsons._load_impl import load


def default_defaultdict_deserializer(
        obj: dict,
        cls: type,
        *,
        key_transformer: Optional[Callable[[str], str]] = None,
        **kwargs) -> dict:
    """
    Deserialize a defaultdict.
    :param obj: the dict that needs deserializing.
    :param key_transformer: a function that transforms the keys to a different
    style (e.g. PascalCase).
    :param cls: not used.
    :param kwargs: any keyword arguments.
    :return: a deserialized defaultdict instance.
    """
    args = get_args(cls)
    default_factory = None
    cls_ = Dict
    if args:
        key, value = get_args(cls)
        cls_ = Dict[key, value]
        default_factory = value
    loaded = load(obj, cls_, key_transformer=key_transformer, **kwargs)
    return defaultdict(default_factory, loaded)
