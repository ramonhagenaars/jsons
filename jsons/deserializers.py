"""
This module contains default deserializers. You can override the
deserialization process of a particular type as follows:

`jsons.set_deserializer(custom_deserializer, SomeClass)`
"""
import inspect
import re
from datetime import datetime, timezone, timedelta
from enum import EnumMeta
from typing import List, Callable
from jsons._common_impl import RFC3339_DATETIME_PATTERN, load_impl, \
    snakecase, camelcase, pascalcase, lispcase


def default_datetime_deserializer(obj: str, _: datetime, **__) -> datetime:
    """
    Deserialize a string with an RFC3339 pattern to a datetime instance.
    :param obj:
    :param _: not used.
    :param __: not used.
    :return: a `datetime.datetime` instance.
    """
    pattern = RFC3339_DATETIME_PATTERN
    if '.' in obj:
        pattern += '.%f'
        # strptime allows a fraction of length 6, so trip the rest (if exists).
        regex_pattern = re.compile(r'(\.[0-9]+)')
        frac = regex_pattern.search(obj).group()
        obj = obj.replace(frac, frac[0:7])
    if obj[-1] == 'Z':
        dattim_str = obj[0:-1]
        dattim_obj = datetime.strptime(dattim_str, pattern)
    else:
        dattim_str, offset = obj.split('+')
        dattim_obj = datetime.strptime(dattim_str, pattern)
        hours, minutes = offset.split(':')
        tz = timezone(offset=timedelta(hours=int(hours), minutes=int(minutes)))
        datetime_list = [dattim_obj.year, dattim_obj.month, dattim_obj.day,
                         dattim_obj.hour, dattim_obj.minute, dattim_obj.second,
                         dattim_obj.microsecond, tz]
        dattim_obj = datetime(*datetime_list)
    return dattim_obj


def default_list_deserializer(obj: List, cls, **kwargs) -> object:
    """
    Deserialize a list by deserializing all items of that list.
    :param obj: the list that needs deserializing.
    :param cls: the type with a generic (e.g. List[str]).
    :param kwargs: any keyword arguments.
    :return: a deserialized list instance.
    """
    cls_ = None
    if cls and hasattr(cls, '__args__'):
        cls_ = cls.__args__[0]
    return [load_impl(x, cls_, **kwargs) for x in obj]


def default_tuple_deserializer(obj: List, cls, **kwargs) -> object:
    """
    Deserialize a (JSON) list into a tuple by deserializing all items of that
    list.
    :param obj: the list that needs deserializing.
    :param cls: the type with a generic (e.g. Tuple[str, int]).
    :param kwargs: any keyword arguments.
    :return: a deserialized tuple instance.
    """
    if hasattr(cls, '__tuple_params__'):
        tuple_types = cls.__tuple_params__
    else:
        tuple_types = cls.__args__
    list_ = [load_impl(obj[i], tuple_types[i], **kwargs)
             for i in range(len(obj))]
    return tuple(list_)


def default_dict_deserializer(obj: dict, _: type,
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
    new_kwargs = {**{'key_transformer': key_transformer}, **kwargs}
    return {key_transformer(key): load_impl(obj[key], **new_kwargs)
            for key in obj}


def default_enum_deserializer(obj: str, cls: EnumMeta,
                              use_enum_name: bool = True, **__) -> object:
    """
    Deserialize an enum value to an enum instance. The serialized value must
    can be the name of the enum element or the value; dependent on
    `use_enum_name`.
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
    Deserialize a string. If the given `obj` can be parsed to a date, a
    `datetime` instance is returned.
    :param obj: the string that is to be deserialized.
    :param _: not used.
    :param kwargs: any keyword arguments.
    :return: the deserialized obj.
    """
    try:
        # Use load_impl instead of default_datetime_deserializer to allow the
        # datetime deserializer to be overridden.
        return load_impl(obj, datetime, **kwargs)
    except:
        return obj


def default_primitive_deserializer(obj: object,
                                   _: type = None, **__) -> object:
    """
    Deserialize a primitive: it simply returns the given primitive.
    :param obj: the value that is to be deserialized.
    :param _: not used.
    :param __: not used.
    :return: `obj`.
    """
    return obj


def default_object_deserializer(obj: dict, cls: type,
                                key_transformer: Callable[[str], str] = None,
                                **kwargs) -> object:
    """
    Deserialize `obj` into an instance of type `cls`. If `obj` contains keys
    with a certain case style (e.g. camelCase) that do not match the style of
    `cls` (e.g. snake_case), a key_transformer should be used (e.g.
    KEY_TRANSFORMER_SNAKECASE).
    :param obj: a serialized instance of `cls`.
    :param cls: the type to which `obj` should be deserialized.
    :param key_transformer: a function that transforms the keys in order to
    match the attribute names of `cls`.
    :param kwargs: any keyword arguments that may be passed to the
    deserializers.
    :return: an instance of type `cls`.
    """
    if key_transformer:
        obj = {key_transformer(key): obj[key] for key in obj}
    signature_parameters = inspect.signature(cls.__init__).parameters
    # Loop through the signature of cls: the type we try to deserialize to. For
    # every required parameter, we try to get the corresponding value from
    # json_obj.
    constructor_args = dict()
    for signature_key, signature in signature_parameters.items():
        if obj and signature_key != 'self':
            if signature_key in obj:
                cls_ = None
                if signature.annotation != inspect._empty:
                    cls_ = signature.annotation
                value = load_impl(obj[signature_key], cls_,
                                  key_transformer=key_transformer, **kwargs)
                constructor_args[signature_key] = value

    # The constructor arguments are gathered, create an instance.
    instance = cls(**constructor_args)
    # Set any remaining attributes on the newly created instance.
    remaining_attrs = {attr_name: obj[attr_name] for attr_name in obj
                       if attr_name not in constructor_args}
    for attr_name in remaining_attrs:
        loaded_attr = load_impl(remaining_attrs[attr_name],
                                type(remaining_attrs[attr_name]),
                                key_transformer=key_transformer, **kwargs)
        setattr(instance, attr_name, loaded_attr)
    return instance


# The following default key transformers can be used with the
# default_object_serializer.
KEY_TRANSFORMER_SNAKECASE = snakecase
KEY_TRANSFORMER_CAMELCASE = camelcase
KEY_TRANSFORMER_PASCALCASE = pascalcase
KEY_TRANSFORMER_LISPCASE = lispcase
