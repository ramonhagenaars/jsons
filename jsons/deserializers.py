"""
This module contains default deserializers. You can override the
deserialization process of a particular type as follows:

``jsons.set_deserializer(custom_deserializer, SomeClass)``
"""
import inspect
import re
from datetime import datetime, timezone, timedelta
from enum import EnumMeta
from typing import List, Callable
from jsons import _common_impl
from jsons._common_impl import RFC3339_DATETIME_PATTERN, snakecase, \
    camelcase, pascalcase, lispcase


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
    dattim_func = _datetime_utc if obj[-1] == 'Z' else _datetime_with_tz
    return dattim_func(obj, pattern)


def _datetime_utc(obj: str, pattern: str):
    dattim_str = obj[0:-1]
    dattim_obj = datetime.strptime(dattim_str, pattern)
    return datetime(dattim_obj.year, dattim_obj.month, dattim_obj.day,
                    dattim_obj.hour, dattim_obj.minute, dattim_obj.second,
                    dattim_obj.microsecond, timezone.utc)


def _datetime_with_tz(obj: str, pattern: str):
    dat_str, tim_str = obj.split('T')
    splitter = '+' if '+' in tim_str else '-'
    naive_tim_str, offset = tim_str.split(splitter)
    naive_dattim_str = '{}T{}'.format(dat_str, naive_tim_str)
    dattim_obj = datetime.strptime(naive_dattim_str, pattern)
    hrs_str, mins_str = offset.split(':')
    hrs = int(hrs_str) if splitter == '+' else -1 * int(hrs_str)
    mins = int(mins_str) if splitter == '+' else -1 * int(mins_str)
    tz = timezone(offset=timedelta(hours=hrs, minutes=mins))
    datetime_list = [dattim_obj.year, dattim_obj.month, dattim_obj.day,
                     dattim_obj.hour, dattim_obj.minute, dattim_obj.second,
                     dattim_obj.microsecond, tz]
    return datetime(*datetime_list)


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
    return [_common_impl.load(x, cls_, **kwargs) for x in obj]


def default_tuple_deserializer(obj: List, cls, **kwargs) -> object:
    """
    Deserialize a (JSON) list into a tuple by deserializing all items of that
    list.
    :param obj: the list that needs deserializing.
    :param cls: the type optionally with a generic (e.g. Tuple[str, int]).
    :param kwargs: any keyword arguments.
    :return: a deserialized tuple instance.
    """
    if hasattr(cls, '__tuple_params__'):
        tuple_types = cls.__tuple_params__
    else:
        tuple_types = cls.__args__
    list_ = [_common_impl.load(obj[i], tuple_types[i], **kwargs)
             for i in range(len(obj))]
    return tuple(list_)


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
    return {key_transformer(key): _common_impl.load(obj[key], **kwargs_)
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
        return _common_impl.load(obj, datetime, **kwargs)
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


def default_object_deserializer(obj: dict, cls: type,
                                key_transformer: Callable[[str], str] = None,
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
    :param kwargs: any keyword arguments that may be passed to the
    deserializers.
    :return: an instance of type ``cls``.
    """
    concat_kwargs = kwargs
    if key_transformer:
        obj = {key_transformer(key): obj[key] for key in obj}
        concat_kwargs = {**kwargs, 'key_transformer': key_transformer}
    signature_parameters = inspect.signature(cls.__init__).parameters
    constructor_args = _get_constructor_args(obj, signature_parameters,
                                             **concat_kwargs)
    remaining_attrs = {attr_name: obj[attr_name] for attr_name in obj
                       if attr_name not in constructor_args}
    instance = cls(**constructor_args)
    _set_remaining_attrs(instance, remaining_attrs, **kwargs)
    return instance


def _get_constructor_args(obj, signature_parameters, **kwargs):
    # Loop through the signature of cls: the type we try to deserialize to. For
    # every required parameter, we try to get the corresponding value from
    # json_obj.
    constructor_args = dict()
    sigs = [(sig_key, sig) for sig_key, sig in signature_parameters.items()
            if obj and sig_key != 'self' and sig_key in obj]
    for sig_key, sig in sigs:
        cls = sig.annotation if sig.annotation != inspect.Parameter.empty \
            else None
        value = _common_impl.load(obj[sig_key], cls, **kwargs)
        constructor_args[sig_key] = value
    return constructor_args


def _set_remaining_attrs(instance, remaining_attrs, **kwargs):
    # Set any remaining attributes on the newly created instance.
    for attr_name in remaining_attrs:
        loaded_attr = _common_impl.load(remaining_attrs[attr_name],
                                             type(remaining_attrs[attr_name]),
                                             **kwargs)
        try:
            setattr(instance, attr_name, loaded_attr)
        except AttributeError:
            pass  # This is raised when a @property does not have a setter.


# The following default key transformers can be used with the
# default_object_serializer.
KEY_TRANSFORMER_SNAKECASE = snakecase
KEY_TRANSFORMER_CAMELCASE = camelcase
KEY_TRANSFORMER_PASCALCASE = pascalcase
KEY_TRANSFORMER_LISPCASE = lispcase
