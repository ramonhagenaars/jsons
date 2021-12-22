from typing import Callable, Optional, Tuple

from typish import get_args

from jsons._load_impl import load
from jsons.exceptions import DeserializationError


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
    cls_args = get_args(cls)

    obj_, keys_were_hashed = _load_hashed_keys(
        obj, cls, cls_args, key_transformer=key_transformer, **kwargs)

    return _deserialize(obj_, cls_args, key_transformer, keys_were_hashed, kwargs)


def _load_hashed_keys(
        obj: dict,
        cls: type,
        cls_args: tuple,
        **kwargs) -> Tuple[dict, bool]:
    # Load any hashed keys and return a copy of the given obj if any hashed
    # keys are unpacked.
    result = obj

    stored_keys = set(obj.get('-keys', set()))
    if stored_keys:
        # Apparently, there are stored hashed keys, we need to unpack them.
        if len(cls_args) != 2:
            raise DeserializationError('A detailed type is needed for cls of '
                                       'the form Dict[<type>, <type>] to '
                                       'deserialize a dict with hashed keys.',
                                       obj, cls)
        result = {**obj}
        key_type = cls_args[0]
        for key in stored_keys:
            # Get the original (unhashed) key and load it.
            original_key = result['-keys'][key]
            loaded_key = load(original_key, cls=key_type, **kwargs)

            # Replace the hashed key by the loaded key entirely.
            result[loaded_key] = result[key]
            del result['-keys'][key]
            del result[key]

        del result['-keys']
    return result, len(stored_keys) > 0


def _deserialize(
        obj: dict,
        cls_args: tuple,
        key_transformer: Callable[[str], str],
        keys_were_hashed: bool,
        kwargs: dict) -> dict:
    key_transformer = key_transformer or (lambda key: key)
    key_func = key_transformer
    kwargs_ = {**kwargs, 'key_transformer': key_transformer}

    if len(cls_args) == 2:
        cls_k, cls_v = cls_args
        kwargs_['cls'] = cls_v
        if not keys_were_hashed:
            # In case of cls is something like Dict[<key>, <value>], we need to
            # ensure that the keys in the result are <key>. If the keys were
            # hashed though, they have been loaded already.
            kwargs_k = {**kwargs, 'cls': cls_k}
            key_func = lambda key: load(key_transformer(key), **kwargs_k)
    return {
        key_func(key): load(obj[key], **kwargs_)
        for key in obj
    }
