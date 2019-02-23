"""
This module contains default deserializers. You can override the
deserialization process of a particular type as follows:

``jsons.set_deserializer(custom_deserializer, SomeClass)``
"""
import inspect
import re
from datetime import datetime
from enum import EnumMeta
from typing import List, Callable
from jsons import _main_impl
from jsons._common_impl import get_class_name
from jsons._datetime_impl import get_datetime_inst
from jsons._main_impl import (
    RFC3339_DATETIME_PATTERN,
    snakecase,
    camelcase,
    pascalcase,
    lispcase
)
from jsons.exceptions import (
    UnfulfilledArgumentError,
    SignatureMismatchError,
    JsonsError,
    DeserializationError
)


def default_datetime_deserializer(obj: str, _: datetime, **__) -> datetime:
    """
    Deserialize a string with an RFC3339 pattern to a datetime instance.
    :param obj:
    :param _: not used.
    :param __: not used.
    :return: a ``datetime.datetime`` instance.
    """
    pattern = RFC3339_DATETIME_PATTERN
    if '.' in obj:
        pattern += '.%f'
        # strptime allows a fraction of length 6, so trip the rest (if exists).
        regex_pattern = re.compile(r'(\.[0-9]+)')
        frac = regex_pattern.search(obj).group()
        obj = obj.replace(frac, frac[0:7])
    return get_datetime_inst(obj, pattern)


def default_list_deserializer(obj: List, cls, **kwargs) -> object:
    """
    Deserialize a list by deserializing all items of that list.
    :param obj: the list that needs deserializing.
    :param cls: the type optionally with a generic (e.g. List[str]).
    :param kwargs: any keyword arguments.
    :return: a deserialized list instance.
    """
    cls_ = None
    if cls and hasattr(cls, '__args__'):
        cls_ = cls.__args__[0]
    return [_main_impl.load(x, cls_, **kwargs) for x in obj]


def default_tuple_deserializer(obj: List, cls, **kwargs) -> object:
    """
    Deserialize a (JSON) list into a tuple by deserializing all items of that
    list.
    :param obj: the list that needs deserializing.
    :param cls: the type optionally with a generic (e.g. Tuple[str, int]).
    :param kwargs: any keyword arguments.
    :return: a deserialized tuple instance.
    """
    tuple_types = getattr(cls, '__tuple_params__', cls.__args__)
    if len(tuple_types) > 1 and tuple_types[1] is ...:
        tuple_types = [tuple_types[0]] * len(obj)
    list_ = [_main_impl.load(value, tuple_types[i], **kwargs)
             for i, value in enumerate(obj)]
    return tuple(list_)


def default_union_deserializer(obj: object, cls, **kwargs) -> object:
    for sub_type in cls.__args__:
        try:
            return _main_impl.load(obj, sub_type, **kwargs)
        except JsonsError:
            pass  # Try the next one.
    else:
        args_msg = ', '.join([get_class_name(cls_) for cls_ in cls.__args__])
        err_msg = ('Could not match the object of type "{}" to any type of '
                   'the Union: {}'.format(str(cls), args_msg))  # TODO use _get_class_name
        raise DeserializationError(err_msg, obj, cls)


def default_set_deserializer(obj: List, cls, **kwargs) -> object:
    """
    Deserialize a (JSON) list into a set by deserializing all items of that
    list.
    :param obj: the list that needs deserializing.
    :param cls: the type optionally with a generic (e.g. Set[str]).
    :param kwargs: any keyword arguments.
    :return: a deserialized set instance.
    """
    cls_ = list
    if hasattr(cls, '__args__'):
        cls_ = List[cls.__args__[0]]
    list_ = default_list_deserializer(obj, cls_, **kwargs)
    return set(list_)


def default_dict_deserializer(obj: dict, cls: type,
                              key_transformer: Callable[[str], str] = None,
                              **kwargs) -> object:
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
    return {key_transformer(key): _main_impl.load(obj[key], **kwargs_)
            for key in obj}


def default_enum_deserializer(obj: str, cls: EnumMeta,
                              use_enum_name: bool = True, **__) -> object:
    """
    Deserialize an enum value to an enum instance. The serialized value must
    can be the name of the enum element or the value; dependent on
    ``use_enum_name``.
    :param obj: the serialized enum.
    :param cls: the enum class.
    :param use_enum_name: determines whether the name or the value of an enum
    element should be used.
    :param __: not used.
    :return: the corresponding enum element instance.
    """
    if use_enum_name:
        result = cls[obj]
    else:
        for elem in cls:
            if elem.value == obj:
                result = elem
                break
    return result


def default_string_deserializer(obj: str, _: type = None, **kwargs) -> object:
    """
    Deserialize a string. If the given ``obj`` can be parsed to a date, a
    ``datetime`` instance is returned.
    :param obj: the string that is to be deserialized.
    :param _: not used.
    :param kwargs: any keyword arguments.
    :return: the deserialized obj.
    """
    try:
        # Use load instead of default_datetime_deserializer to allow the
        # datetime deserializer to be overridden.
        return _main_impl.load(obj, datetime, **kwargs)
    except:
        return obj


def default_primitive_deserializer(obj: object,
                                   _: type = None, **__) -> object:
    """
    Deserialize a primitive: it simply returns the given primitive.
    :param obj: the value that is to be deserialized.
    :param _: not used.
    :param __: not used.
    :return: ``obj``.
    """
    return obj


def default_object_deserializer(obj: dict,
                                cls: type,
                                key_transformer: Callable[[str], str] = None,
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
    signature_parameters = inspect.signature(cls.__init__).parameters
    constructor_args, getters = _get_constructor_args(obj,
                                                      cls,
                                                      signature_parameters,
                                                      **concat_kwargs)
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


def _get_constructor_args(obj,
                          cls,
                          signature_parameters,
                          attr_getters=None,
                          **kwargs):
    # Loop through the signature of cls: the type we try to deserialize to. For
    # every required parameter, we try to get the corresponding value from
    # json_obj.
    attr_getters = dict(**(attr_getters or {}))
    constructor_args_in_obj = dict()
    signatures = ((sig_key, sig) for sig_key, sig in
                  signature_parameters.items() if sig_key != 'self')
    for sig_key, sig in signatures:
        if obj and sig_key in obj:
            # This argument is in obj.
            arg_cls = None
            if sig.annotation != inspect.Parameter.empty:
                arg_cls = sig.annotation
            value = _main_impl.load(obj[sig_key], arg_cls, **kwargs)
            constructor_args_in_obj[sig_key] = value
        elif sig_key in attr_getters:
            # There exists an attr_getter for this argument.
            attr_getter = attr_getters.pop(sig_key)
            constructor_args_in_obj[sig_key] = attr_getter()
        elif sig.default != inspect.Parameter.empty:
            # There is a default value for this argument.
            constructor_args_in_obj[sig_key] = sig.default
        elif sig.kind not in (inspect.Parameter.VAR_POSITIONAL,
                              inspect.Parameter.VAR_KEYWORD):
            # This argument is no *args or **kwargs and has no value.
            raise UnfulfilledArgumentError(
                'No value found for "{}"'.format(sig_key),
                sig_key, obj, cls)

    return constructor_args_in_obj, attr_getters


def _set_remaining_attrs(instance,
                         remaining_attrs,
                         attr_getters=None,
                         **kwargs):
    # Set any remaining attributes on the newly created instance.
    attr_getters = attr_getters or {}
    for attr_name in remaining_attrs:
        loaded_attr = _main_impl.load(remaining_attrs[attr_name],
                                      type(remaining_attrs[attr_name]),
                                      **kwargs)
        try:
            setattr(instance, attr_name, loaded_attr)
        except AttributeError:
            pass  # This is raised when a @property does not have a setter.
    for attr_name, getter in attr_getters.items():
        setattr(instance, attr_name, getter())


# The following default key transformers can be used with the
# default_object_serializer.
KEY_TRANSFORMER_SNAKECASE = snakecase
KEY_TRANSFORMER_CAMELCASE = camelcase
KEY_TRANSFORMER_PASCALCASE = pascalcase
KEY_TRANSFORMER_LISPCASE = lispcase
