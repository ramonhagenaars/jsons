from typing import Callable, Optional, Tuple

from jsons._common_impl import JSON_KEYS
from jsons._load_impl import load
from jsons.exceptions import DeserializationError

from typish import get_args


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
    kwargs_ = {**kwargs, 'key_transformer': key_transformer}

    (obj_, had_stored_keys) = _load_hashed_keys(obj, cls, cls_args,
                                                key_transformer=key_transformer, **kwargs)

    if len(cls_args) == 2:
        cls_k, cls_v = cls_args
        kwargs_k = {**kwargs_, 'cls': cls_k}
        kwargs_v = {**kwargs_, 'cls': cls_v}
        if (had_stored_keys and
                not any(issubclass(type(cls_k), json_key) for json_key in JSON_KEYS)):
            # There were hashed keys and the key is not a json key, therefore
            # the key must have been hashed and therefore loaded already during _load_hashed_keys
            # double deserializing under strict will fail, so avoid doing so.
            res = {key_tfr(k): load(obj_[k], **kwargs_v)
                   for k in obj_}
        else:
            # The key was either inherently json compatible or serialized to be so, thus
            # avoiding hashed keys
            res = {load(key_tfr(k), **kwargs_k): load(obj_[k], **kwargs_v)
                   for k in obj_}
    else:
        res = {key_tfr(key): load(obj_[key], **kwargs_)
               for key in obj_}
    return res


def _load_hashed_keys(obj: dict, cls: type, cls_args: tuple, **kwargs) -> Tuple[dict, bool]:
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
    return (result, len(stored_keys) > 0)
