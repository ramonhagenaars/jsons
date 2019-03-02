import inspect
from functools import partial
from typing import Optional, Callable
from jsons._common_impl import get_class_name
from jsons._main_impl import load
from jsons.exceptions import SignatureMismatchError, UnfulfilledArgumentError


def default_object_deserializer(
        obj: dict,
        cls: type,
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
    concat_kwargs = kwargs
    if key_transformer:
        obj = {key_transformer(key): obj[key] for key in obj}
        concat_kwargs = {
            **kwargs,
            'key_transformer': key_transformer
        }
    concat_kwargs['strict'] = strict
    constructor_args = _get_constructor_args(obj, cls, **concat_kwargs)
    remaining_attrs = {attr_name: obj[attr_name] for attr_name in obj
                       if attr_name not in constructor_args}
    if strict and remaining_attrs:
        unexpected_arg = list(remaining_attrs.keys())[0]
        err_msg = 'Type "{}" does not expect "{}"'.format(get_class_name(cls),
                                                          unexpected_arg)
        raise SignatureMismatchError(err_msg, unexpected_arg, obj, cls)
    instance = cls(**constructor_args)
    _set_remaining_attrs(instance, remaining_attrs, **kwargs)
    return instance


def _get_constructor_args(obj, cls, attr_getters=None, **kwargs):
    # Loop through the signature of cls: the type we try to deserialize to. For
    # every required parameter, we try to get the corresponding value from
    # json_obj.
    signature_parameters = inspect.signature(cls.__init__).parameters
    attr_getters = dict(**(attr_getters or {}))
    value_for_attr_part = partial(_get_value_for_attr, obj=obj, cls=cls,
                                  attr_getters=attr_getters, **kwargs)
    args_gen = (value_for_attr_part(sig_key=sig_key, sig=sig) for sig_key, sig
                in signature_parameters.items() if sig_key != 'self')
    constructor_args_in_obj = {key: value for key, value in args_gen if key}
    return constructor_args_in_obj


def _get_value_for_attr(obj, cls, sig_key, sig, attr_getters, **kwargs):
    result = None, None
    if obj and sig_key in obj:
        # This argument is in obj.
        arg_cls = None
        if sig.annotation != inspect.Parameter.empty:
            arg_cls = sig.annotation
        value = load(obj[sig_key], arg_cls, **kwargs)
        result = sig_key, value
    elif sig_key in attr_getters:
        # There exists an attr_getter for this argument.
        attr_getter = attr_getters.pop(sig_key)
        result = sig_key, attr_getter()
    elif sig.default != inspect.Parameter.empty:
        # There is a default value for this argument.
        result = sig_key, sig.default
    elif sig.kind not in (inspect.Parameter.VAR_POSITIONAL,
                          inspect.Parameter.VAR_KEYWORD):
        # This argument is no *args or **kwargs and has no value.
        raise UnfulfilledArgumentError(
            'No value found for "{}"'.format(sig_key), sig_key, obj, cls)
    return result


def _set_remaining_attrs(instance,
                         remaining_attrs,
                         attr_getters=None,
                         **kwargs):
    # Set any remaining attributes on the newly created instance.
    attr_getters = attr_getters or {}
    for attr_name in remaining_attrs:
        loaded_attr = load(remaining_attrs[attr_name],
                           type(remaining_attrs[attr_name]),
                           **kwargs)
        try:
            setattr(instance, attr_name, loaded_attr)
        except AttributeError:
            pass  # This is raised when a @property does not have a setter.
    for attr_name, getter in attr_getters.items():
        setattr(instance, attr_name, getter())
