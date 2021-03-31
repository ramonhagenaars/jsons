import inspect
from typing import Optional, Callable, Tuple

from jsons._cache import cached
from jsons._common_impl import (
    get_class_name,
    META_ATTR,
    get_cls_from_str,
    determine_precedence,
    can_match_with_none
)
from jsons._compatibility_impl import get_type_hints
from jsons._load_impl import load
from jsons.exceptions import SignatureMismatchError, UnfulfilledArgumentError


def default_object_deserializer(
        obj: dict,
        cls: type,
        *,
        key_transformer: Optional[Callable[[str], str]] = None,
        strict: bool = False,
        **kwargs) -> object:
    """
    Deserialize ``obj`` into an instance of type ``cls``. If ``obj`` contains
    keys with a certain case style (e.g. camelCase) that do not match the style
    of ``cls`` (e.g. snake_case), a key_transformer should be used (e.g.
    KEY_TRANSFORMER_SNAKECASE).
    :param obj: a serialized instance of ``cls``.
    :param cls: the type to which ``obj`` should be deserialized.
    :param key_transformer: a function that transforms the keys in order to
    match the attribute names of ``cls``.
    :param strict: deserialize in strict mode.
    :param kwargs: any keyword arguments that may be passed to the
    deserializers.
    :return: an instance of type ``cls``.
    """
    obj, kwargs = _check_and_transform_keys(obj, key_transformer, **kwargs)
    kwargs['strict'] = strict
    constructor_args = _get_constructor_args(obj, cls, **kwargs)
    remaining_attrs = _get_remaining_args(obj, cls, constructor_args,
                                          strict, kwargs['fork_inst'])
    instance = cls(**constructor_args)
    _set_remaining_attrs(instance, remaining_attrs, **kwargs)
    return instance


def _get_constructor_args(
        obj,
        cls,
        meta_hints,
        attr_getters=None,
        **kwargs) -> dict:
    # Loop through the signature of cls: the type we try to deserialize to. For
    # every required parameter, we try to get the corresponding value from
    # json_obj.
    signature_parameters = _get_signature(cls)
    hints = get_type_hints(cls.__init__, fallback_ns=cls.__module__)
    attr_getters = dict(**(attr_getters or {}))

    result = {}
    for sig_key, sig in signature_parameters.items():
        if sig_key != 'self':
            key, value = _get_value_for_attr(obj=obj,
                                             orig_cls=cls,
                                             meta_hints=meta_hints,
                                             attr_getters=attr_getters,
                                             sig_key=sig_key,
                                             cls=hints.get(sig_key, None),
                                             sig=sig,
                                             **kwargs)
            if key:
                result[key] = value
    return result


@cached
def _get_signature(cls):
    return inspect.signature(cls.__init__).parameters


def _get_value_for_attr(
        obj,
        cls,
        orig_cls,
        sig_key,
        sig,
        meta_hints,
        attr_getters,
        **kwargs):
    # Find a value for the attribute (with signature sig_key).
    if obj and sig_key in obj:
        # This argument is in obj.
        result = sig_key, _get_value_from_obj(obj, cls, sig, sig_key,
                                              meta_hints, **kwargs)
    elif sig_key in attr_getters:
        # There exists an attr_getter for this argument.
        attr_getter = attr_getters.pop(sig_key)
        result = sig_key, attr_getter()
    elif sig.default != inspect.Parameter.empty:
        # There is a default value for this argument.
        result = sig_key, sig.default
    elif sig.kind in (inspect.Parameter.VAR_POSITIONAL,
                      inspect.Parameter.VAR_KEYWORD):
        # This argument is either *args or **kwargs.
        result = None, None
    elif can_match_with_none(cls):
        # It is fine that there is no value.
        result = sig_key, None
    else:
        raise UnfulfilledArgumentError(
            'No value found for "{}".'.format(sig_key), sig_key, obj, orig_cls)
    return result


def _remove_prefix(prefix: str, s: str) -> str:
    if s.startswith(prefix):
        return s[len(prefix):] or '/'  # Special case: map the empty string to '/'
    return s


def _get_value_from_obj(obj, cls, sig, sig_key, meta_hints, **kwargs):
    # Obtain the value for the attribute with the given signature from the
    # given obj. Try to obtain the class of this attribute from the meta info
    # or from type hints.
    cls_key = '/{}'.format(sig_key)
    cls_str_from_meta = meta_hints.get(cls_key, None)
    new_hints = meta_hints
    cls_from_meta = None
    if cls_str_from_meta:
        cls_from_meta = get_cls_from_str(
            cls_str_from_meta, obj, kwargs['fork_inst'])
        # Rebuild the class hints: cls_key becomes the new root.
        new_hints = {
            _remove_prefix(cls_key, key): meta_hints[key]
            for key in meta_hints
        }
    cls_ = determine_precedence(cls=cls, cls_from_meta=cls_from_meta,
                                cls_from_type=None, inferred_cls=True)
    value = load(obj[sig_key], cls_, meta_hints=new_hints, **kwargs)
    return value


def _set_remaining_attrs(instance,
                         remaining_attrs,
                         attr_getters,
                         **kwargs):
    # Set any remaining attributes on the newly created instance.
    attr_getters = attr_getters or {}
    for attr_name in remaining_attrs:
        annotations = get_type_hints(instance.__class__)
        attr_type = annotations.get(attr_name)

        if isinstance(remaining_attrs[attr_name], dict) \
                and '-keys' in remaining_attrs[attr_name] \
                and not attr_type:
            fork_inst = kwargs['fork_inst']
            fork_inst._warn('A dict with -keys was detected without a type '
                            'hint for attribute `{}`. This probably means '
                            'that you did not provide an annotation in your '
                            'class (ending up in __annotations__).'
                            .format(attr_name), 'hashed-keys-without-hint')
        attr_type = attr_type or type(remaining_attrs[attr_name])

        loaded_attr = load(remaining_attrs[attr_name], attr_type, **kwargs)
        try:
            setattr(instance, attr_name, loaded_attr)
        except AttributeError:
            pass  # This is raised when a @property does not have a setter.
    for attr_name, getter in attr_getters.items():
        setattr(instance, attr_name, getter())


def _check_and_transform_keys(obj: dict,
                              key_transformer: Optional[Callable[[str], str]],
                              **kwargs) -> Tuple[dict, dict]:
    if key_transformer:
        obj = {key_transformer(key): obj[key] for key in obj}
        kwargs = {
            **kwargs,
            'key_transformer': key_transformer
        }
    return obj, kwargs


def _get_remaining_args(obj: dict,
                        cls: type,
                        constructor_args: dict,
                        strict: bool,
                        fork_inst: type) -> dict:
    # Get the remaining args or raise if strict and the signature is unmatched.
    remaining_attrs = {attr_name: obj[attr_name] for attr_name in obj
                       if attr_name not in constructor_args
                       and attr_name != META_ATTR}
    if strict and remaining_attrs:
        unexpected_arg = list(remaining_attrs.keys())[0]
        err_msg = ('Type "{}" does not expect "{}".'
                   .format(get_class_name(cls), unexpected_arg))
        raise SignatureMismatchError(err_msg, unexpected_arg, obj, cls)
    return remaining_attrs
