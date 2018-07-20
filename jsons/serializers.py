"""
This module contains default serializers. You can override the serialization
process of a particular type as follows:

`jsons.set_serializer(custom_deserializer, SomeClass)`
"""
from datetime import datetime
from enum import EnumMeta
from typing import Callable
from jsons import dump_impl
from jsons._common_impl import RFC3339_DATETIME_PATTERN, snakecase, \
    camelcase, pascalcase, lispcase


def default_list_serializer(obj: list, **kwargs) -> list:
    """
    Serialize the given `obj` to a list of serialized objects.
    :param obj: the list that is to be serialized.
    :param kwargs: any keyword arguments that may be given to the serialization
    process.
    :return: a list of which all elements are serialized.
    """
    return [dump_impl(elem, **kwargs) for elem in obj]


def default_dict_serializer(obj: list, **kwargs) -> dict:
    """
    Serialize the given `obj` to a dict of serialized objects.
    :param obj: the dict that is to be serialized.
    :param kwargs: any keyword arguments that may be given to the serialization
    process.
    :return: a dict of which all elements are serialized.
    """
    return {key: dump_impl(obj[key], **kwargs) for key in obj}


def default_enum_serializer(obj: EnumMeta, use_enum_name: bool = True,
                            **_) -> str:
    """
    Serialize the given obj. By default, the name of the enum element is
    returned.
    :param obj: an instance of an enum.
    :param use_enum_name: determines whether the name or the value should be
    used for serialization.
    :param _: not used.
    :return: `obj` serialized as a string.
    """
    attr = 'name' if use_enum_name else 'value'
    return getattr(obj, attr)


def default_datetime_serializer(obj: datetime, **_) -> str:
    """
    Serialize the given datetime instance to a string. It uses the RFC3339
    pattern. If datetime is a localtime, an offset is provided. If datetime is
    in UTC, the result is suffixed with a 'Z'.
    :param obj: the datetime instance that is to be serialized.
    :param _: not used.
    :return: `datetime` as an RFC3339 string.
    """
    timezone = obj.tzinfo
    offset = 'Z'
    pattern = RFC3339_DATETIME_PATTERN
    if timezone:
        if timezone.tzname(None) != 'UTC':
            offset = timezone.tzname(None).split('UTC')[1]
    if obj.microsecond:
        pattern += '.%f'
    return obj.strftime("{}{}".format(pattern, offset))


def default_primitive_serializer(obj, **_) -> object:
    """
    Serialize a primitive; simply return the given `obj`.
    :param obj:
    :param _: not used.
    :return: `obj`.
    """
    return obj


def default_object_serializer(obj: object,
                              key_transformer: Callable[[str], str] = None,
                              **kwargs) -> dict:
    """
    Serialize the given `obj` to a dict. All values within `obj` are also
    serialized. If `key_transformer` is given, it will be used to transform the
    casing (e.g. snake_case) to a different format (e.g. camelCase).
    :param obj: the object that is to be serialized.
    :param key_transformer: a function that will be applied to all keys in the
    resulting dict.
    :param kwargs: any keyword arguments that are to be passed to the
    serializer functions.
    :return: a Python dict holding the values of `obj`.
    """
    d = obj.__dict__
    key_transformer_ = key_transformer or (lambda key: key)
    return {key_transformer_(key): dump_impl(d[key],
                                             key_transformer=key_transformer,
                                             **kwargs) for key in d}


# The following default key transformers can be used with the
# default_object_serializer.
KEY_TRANSFORMER_SNAKECASE = snakecase
KEY_TRANSFORMER_CAMELCASE = camelcase
KEY_TRANSFORMER_PASCALCASE = pascalcase
KEY_TRANSFORMER_LISPCASE = lispcase
