from typing import Callable, Dict, Optional, Tuple

from jsons._common_impl import JSON_KEYS
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

        # If key is not a valid json type, use the hash as key and store the
        # original key in a separate section.
        dict_and_key = _store_and_hash(result, key,
                                       key_transformer=key_transformer,
                                       strip_nulls=strip_nulls, strict=strict,
                                       types=types, **kwargs)
        if dict_and_key:
            result, key = dict_and_key

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


def _store_and_hash(
        obj: dict,
        key: object,
        **kwargs
) -> Optional[Tuple[dict, int]]:
    # Store the given key in the given dict under a special section if that
    # key is not a valid json key. Return a hash of that key.
    result = None
    if not _is_valid_json_key(key):
        # First try to dump the key, that might be enough already.
        dumped_key = dump(key, **kwargs)
        result = obj, dumped_key
        if not _is_valid_json_key(dumped_key):
            # Apparently, this was not enough; the key is still not "jsonable".
            key_hash = hash(key)
            obj_ = {**obj}
            obj_.setdefault('-keys', {})
            obj_['-keys'][key_hash] = dumped_key
            result = obj_, key_hash
    return result


def _is_valid_json_key(key: object) -> bool:
    return any(issubclass(type(key), json_key) for json_key in JSON_KEYS)
