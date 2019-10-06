from typing import Optional, Callable
from typish import get_args
from jsons._load_impl import load


def default_dict_deserializer(
        obj: dict,
        cls: type,
        *,
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
    key_tfr = key_transformer or (lambda key: key)
    cls_args = get_args(cls)
    if len(cls_args) == 2:
        cls_k, cls_v = cls_args
        kwargs_k = {**kwargs, 'cls': cls_k}
        kwargs_v = {**kwargs, 'cls': cls_v}
        res = {load(key_tfr(k), **kwargs_k): load(obj[k], **kwargs_v)
               for k in obj}
    else:
        res = {key_tfr(key): load(obj[key], **kwargs)
               for key in obj}
    return res
