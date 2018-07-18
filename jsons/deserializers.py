import inspect
import re
from datetime import datetime, timezone, timedelta
from enum import Enum, EnumMeta
from typing import List, Callable
from jsons._common_impl import RFC3339_DATETIME_PATTERN, load_impl, \
    snakecase, camelcase, pascalcase, lispcase


def default_datetime_deserializer(obj: str, _: datetime, **__) -> datetime:
    pattern = RFC3339_DATETIME_PATTERN
    if '.' in obj:
        pattern += '.%f'
        # strptime allows a fraction of length 6, so trip the rest (if exists).
        regex_pattern = re.compile('(\.[0-9]+)')
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
    cls_ = None
    if cls and hasattr(cls, '__args__'):
        cls_ = cls.__args__[0]
    return [load_impl(x, cls_, **kwargs) for x in obj]


def default_enum_deserializer(obj: Enum, cls: EnumMeta, **__) -> object:
    return cls[obj]


def default_string_deserializer(obj: str, _: type = None, **kwargs) -> object:
    try:
        return load_impl(obj, datetime, **kwargs)
    except:
        return obj


def default_primitive_deserializer(obj: object,
                                   _: type = None, **__) -> object:
    return obj


def default_object_deserializer(obj: dict, cls: type,
                                key_transformer: Callable[[str], str] = None,
                                **kwargs) -> object:
    if key_transformer:
        obj = {key_transformer(key): obj[key] for key in obj}
    signature_parameters = inspect.signature(cls.__init__).parameters
    # Loop through the signature of cls: the type we try to deserialize to. For
    # every required parameter, we try to get the corresponding value from
    # json_obj.
    constructor_args = dict()
    for signature_key, signature in signature_parameters.items():
        if obj and signature_key is not 'self':
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
