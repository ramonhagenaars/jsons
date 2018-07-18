from datetime import datetime
from enum import EnumMeta
from jsons import dump_impl
from jsons._common_impl import RFC3339_DATETIME_PATTERN


def default_list_serializer(obj: list, **kwargs) -> dict:
    return [dump_impl(elem, **kwargs) for elem in obj]


def default_enum_serializer(obj: EnumMeta, **_) -> dict:
    return obj.name


def default_datetime_serializer(obj: datetime, **_) -> dict:
    timezone = obj.tzinfo
    offset = 'Z'
    pattern = RFC3339_DATETIME_PATTERN
    if timezone:
        if timezone.tzname(None) != 'UTC':
            offset = timezone.tzname(None).split('UTC')[1]
    if obj.microsecond:
        pattern += '.%f'
    return obj.strftime("{}{}".format(pattern, offset))


def default_primitive_serializer(obj, **_) -> dict:
    return obj


def default_object_serializer(obj, **kwargs) -> dict:
    d = obj.__dict__
    return {key: dump_impl(d[key], **kwargs) for key in d}
