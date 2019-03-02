from typing import Optional, Callable
from jsons._main_impl import load


def default_dict_deserializer(
        obj: dict,
        cls: type,
        key_transformer: Optional[Callable[[str], str]] = None,
        **kwargs) -> dict:
    """
    Deserialize a dict by deserializing all instances of that dict.
    :param obj: the dict that needs deserializing.
    :param key_transformer: a function that transforms the keys to a different
    style (e.g. PascalCase).
    :param cls: not used.
    :param kwargs: any keyword arguments.
    :return: a deserialized dict instance.
    """
    key_transformer = key_transformer or (lambda key: key)
    kwargs_ = {**{'key_transformer': key_transformer}, **kwargs}
    if hasattr(cls, '__args__') and len(cls.__args__) > 1:
        sub_cls = cls.__args__[1]
        kwargs_['cls'] = sub_cls
    return {key_transformer(key): load(obj[key], **kwargs_)
            for key in obj}
