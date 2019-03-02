from typing import Optional, Callable
from jsons._main_impl import dump


def default_dict_serializer(
        obj: dict,
        cls: Optional[type] = None,
        strip_nulls: bool = False,
        key_transformer: Optional[Callable[[str], str]] = None,
        **kwargs) -> dict:
    """
    Serialize the given ``obj`` to a dict of serialized objects.
    :param obj: the dict that is to be serialized.
    :param key_transformer: a function that will be applied to all keys in the
    resulting dict.
    :param strip_nulls: if ``True`` the resulting dict will not contain null
    values.
    :param kwargs: any keyword arguments that may be given to the serialization
    process.
    :return: a dict of which all elements are serialized.
    """
    result = dict()
    for key in obj:
        dumped_elem = dump(obj[key], key_transformer=key_transformer,
                           strip_nulls=strip_nulls, **kwargs)
        if not (strip_nulls and dumped_elem is None):
            if key_transformer:
                key = key_transformer(key)
            result[key] = dumped_elem
    return result
