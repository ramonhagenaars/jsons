from typing import Optional, Callable, Dict

from jsons._dump_impl import dump


def default_dict_serializer(
        obj: dict,
        cls: Optional[type] = None,
        *,
        strict: bool = False,
        strip_nulls: bool = False,
        key_transformer: Optional[Callable[[str], str]] = None,
        types: Optional[Dict[str, type]] = None,
        **kwargs) -> dict:
    """
    Serialize the given ``obj`` to a dict of serialized objects.
    :param obj: the dict that is to be serialized.
    :param cls: not used.
    :param strict: if ``True`` the serialization will raise upon any the
    failure of any attribute. Otherwise it continues with a warning.
    :param strict: a bool to determine if the serializer should be strict
    (i.e. only dumping stuff that is known to ``cls``).
    :param strip_nulls: if ``True`` the resulting dict will not contain null
    values.
    :param key_transformer: a function that will be applied to all keys in the
    resulting dict.
    :param types: a ``dict`` with attribute names (keys) and their types
    (values).
    :param kwargs: any keyword arguments that may be given to the serialization
    process.
    :return: a dict of which all elements are serialized.
    """
    result = dict()
    types = types or dict()
    for key in obj:
        obj_ = obj[key]
        cls_ = types.get(key, None)
        dumped_elem = dump(obj_,
                           cls=cls_,
                           key_transformer=key_transformer,
                           strip_nulls=strip_nulls,
                           strict=strict,
                           **kwargs)
        if not (strip_nulls and dumped_elem is None):
            if key_transformer:
                key = key_transformer(key)
            result[key] = dumped_elem
    return result
