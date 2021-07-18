"""
Works with Python3.5+

JSON (de)serialization (jsons) from and to dicts and plain old Python objects.

Works with dataclasses (Python3.7+).


**Example:**

    >>> from dataclasses import dataclass
    >>> @dataclass
    ... class Car:
    ...     color: str
    >>> @dataclass
    ... class Person:
    ...     car: Car
    ...     name: str
    >>> c = Car('Red')
    >>> p = Person(c, 'John')
    >>> dumped = dump(p)
    >>> dumped['name']
    'John'
    >>> dumped['car']['color']
    'Red'
    >>> p_reloaded = load(dumped, Person)
    >>> p_reloaded.name
    'John'
    >>> p_reloaded.car.color
    'Red'


Deserialization will work with older Python classes (Python3.5+) given that
type hints are present for custom types (i.e. any type that is not set at
the bottom of this module). Serialization will work with no type hints at
all.


**Example**

    >>> class Car:
    ...     def __init__(self, color):
    ...         self.color = color
    >>> class Person:
    ...     def __init__(self, car: Car, name):
    ...         self.car = car
    ...         self.name = name
    >>> c = Car('Red')
    >>> p = Person(c, 'John')
    >>> dumped = dump(p)
    >>> dumped['name']
    'John'
    >>> dumped['car']['color']
    'Red'
    >>> p_reloaded = load(dumped, Person)
    >>> p_reloaded.name
    'John'
    >>> p_reloaded.car.color
    'Red'


Alternatively, you can make use of the `JsonSerializable` class.


**Example**

    >>> class Car(JsonSerializable):
    ...     def __init__(self, color):
    ...         self.color = color
    >>> class Person(JsonSerializable):
    ...     def __init__(self, car: Car, name):
    ...         self.car = car
    ...         self.name = name
    >>> c = Car('Red')
    >>> p = Person(c, 'John')
    >>> dumped = p.json
    >>> dumped['name']
    'John'
    >>> dumped['car']['color']
    'Red'
    >>> p_reloaded = Person.from_json(dumped)
    >>> p_reloaded.name
    'John'
    >>> p_reloaded.car.color
    'Red'

"""
from collections.abc import Mapping
from datetime import datetime, date, time, timezone, timedelta
from decimal import Decimal
from enum import Enum
from pathlib import PurePath
from typing import Union, List, Tuple, Iterable, Optional, DefaultDict, Dict
from uuid import UUID

from jsons._common_impl import NoneType
from jsons._dump_impl import (
    dump,
    dumps,
    dumpb,
)
from jsons._extra_impl import (
    announce_class,
    suppress_warnings,
    suppress_warning,
)
from jsons._fork_impl import fork
from jsons._key_transformers import (
    camelcase,
    snakecase,
    pascalcase,
    lispcase,
)
from jsons._lizers_impl import (
    get_serializer,
    get_deserializer,
    set_serializer,
    set_deserializer,
)
from jsons._load_impl import (
    load,
    loads,
    loadb,
)
from jsons._meta import __version__
from jsons._transform_impl import transform
from jsons._validation import (
    validate,
    get_validator,
    set_validator,
)
from jsons.classes.json_serializable import JsonSerializable
from jsons.classes.verbosity import Verbosity
from jsons.deserializers.default_complex import default_complex_deserializer
from jsons.deserializers.default_date import default_date_deserializer
from jsons.deserializers.default_datetime import default_datetime_deserializer
from jsons.deserializers.default_decimal import default_decimal_deserializer
from jsons.deserializers.default_defaultdict import default_defaultdict_deserializer
from jsons.deserializers.default_dict import default_dict_deserializer
from jsons.deserializers.default_enum import default_enum_deserializer
from jsons.deserializers.default_iterable import default_iterable_deserializer
from jsons.deserializers.default_list import default_list_deserializer
from jsons.deserializers.default_mapping import default_mapping_deserializer
from jsons.deserializers.default_nonetype import default_nonetype_deserializer
from jsons.deserializers.default_object import default_object_deserializer
from jsons.deserializers.default_path import default_path_deserializer
from jsons.deserializers.default_primitive import default_primitive_deserializer
from jsons.deserializers.default_string import default_string_deserializer
from jsons.deserializers.default_time import default_time_deserializer
from jsons.deserializers.default_timedelta import default_timedelta_deserializer
from jsons.deserializers.default_timezone import default_timezone_deserializer
from jsons.deserializers.default_tuple import default_tuple_deserializer
from jsons.deserializers.default_union import default_union_deserializer
from jsons.deserializers.default_uuid import default_uuid_deserializer
from jsons.deserializers.default_zone_info import default_zone_info_deserializer
from jsons.exceptions import (
    JsonsError,
    ValidationError,
    SerializationError,
    DeserializationError,
    DecodeError,
    UnfulfilledArgumentError,
    InvalidDecorationError
)
from jsons.serializers.default_complex import default_complex_serializer
from jsons.serializers.default_date import default_date_serializer
from jsons.serializers.default_datetime import default_datetime_serializer
from jsons.serializers.default_decimal import default_decimal_serializer
from jsons.serializers.default_dict import default_dict_serializer
from jsons.serializers.default_enum import default_enum_serializer
from jsons.serializers.default_iterable import default_iterable_serializer
from jsons.serializers.default_list import default_list_serializer
from jsons.serializers.default_object import default_object_serializer
from jsons.serializers.default_path import default_path_serializer
from jsons.serializers.default_primitive import default_primitive_serializer
from jsons.serializers.default_time import default_time_serializer
from jsons.serializers.default_timedelta import default_timedelta_serializer
from jsons.serializers.default_timezone import default_timezone_serializer
from jsons.serializers.default_tuple import default_tuple_serializer
from jsons.serializers.default_union import default_union_serializer
from jsons.serializers.default_uuid import default_uuid_serializer
from jsons.serializers.default_zone_info import default_zone_info_serializer

KEY_TRANSFORMER_SNAKECASE = snakecase
KEY_TRANSFORMER_CAMELCASE = camelcase
KEY_TRANSFORMER_PASCALCASE = pascalcase
KEY_TRANSFORMER_LISPCASE = lispcase

__all__ = [
    # Functions:
    '__version__',
    dump.__name__,
    dumps.__name__,
    dumpb.__name__,
    load.__name__,
    loads.__name__,
    loadb.__name__,
    transform.__name__,
    fork.__name__,
    set_serializer.__name__,
    'get_serializer',
    set_deserializer.__name__,
    'get_deserializer',
    'get_validator',
    set_validator.__name__,
    validate.__name__,
    'announce_class',
    suppress_warnings.__name__,
    suppress_warning.__name__,

    # Types:
    JsonSerializable.__name__,
    Verbosity.__name__,

    # Key transformers:
    snakecase.__name__,
    camelcase.__name__,
    pascalcase.__name__,
    lispcase.__name__,
    'KEY_TRANSFORMER_SNAKECASE',
    'KEY_TRANSFORMER_CAMELCASE',
    'KEY_TRANSFORMER_PASCALCASE',
    'KEY_TRANSFORMER_LISPCASE',

    # Errors:
    JsonsError.__name__,
    ValidationError.__name__,
    SerializationError.__name__,
    DeserializationError.__name__,
    DecodeError.__name__,
    UnfulfilledArgumentError.__name__,
    InvalidDecorationError.__name__,

    # Serializers:
    default_tuple_serializer.__name__,
    default_dict_serializer.__name__,
    default_iterable_serializer.__name__,
    default_list_serializer.__name__,
    default_enum_serializer.__name__,
    default_complex_serializer.__name__,
    default_datetime_serializer.__name__,
    default_date_serializer.__name__,
    default_time_serializer.__name__,
    default_timezone_serializer.__name__,
    default_timedelta_serializer.__name__,
    default_primitive_serializer.__name__,
    default_object_serializer.__name__,
    default_decimal_serializer.__name__,
    default_uuid_serializer.__name__,
    default_union_serializer.__name__,
    default_path_serializer.__name__,

    # Deserializers:
    default_list_deserializer.__name__,
    default_tuple_deserializer.__name__,
    default_union_deserializer.__name__,
    default_dict_deserializer.__name__,
    default_defaultdict_deserializer.__name__,
    default_enum_deserializer.__name__,
    default_complex_deserializer.__name__,
    default_datetime_deserializer.__name__,
    default_date_deserializer.__name__,
    default_time_deserializer.__name__,
    default_timezone_deserializer.__name__,
    default_timedelta_deserializer.__name__,
    default_string_deserializer.__name__,
    default_nonetype_deserializer.__name__,
    default_primitive_deserializer.__name__,
    default_mapping_deserializer.__name__,
    default_iterable_deserializer.__name__,
    default_object_deserializer.__name__,
    default_uuid_deserializer.__name__,
    default_decimal_deserializer.__name__,
    default_path_deserializer.__name__,
]

set_serializer(default_tuple_serializer, (tuple, Tuple))
set_serializer(default_enum_serializer, Enum)
set_serializer(default_complex_serializer, complex)
set_serializer(default_datetime_serializer, datetime)
set_serializer(default_date_serializer, date)
set_serializer(default_time_serializer, time)
set_serializer(default_timezone_serializer, timezone)
set_serializer(default_timedelta_serializer, timedelta)
set_serializer(default_primitive_serializer, (str, int, float, bool, None))
set_serializer(default_dict_serializer, Mapping, False)
set_serializer(default_list_serializer, (list, List))
set_serializer(default_iterable_serializer, Iterable, False)
set_serializer(default_object_serializer, object, False)
set_serializer(default_uuid_serializer, UUID)
set_serializer(default_decimal_serializer, Decimal)
set_serializer(default_union_serializer, (Union, Optional))
set_serializer(default_path_serializer, PurePath)

set_deserializer(default_list_deserializer, (list, List))
set_deserializer(default_tuple_deserializer, (tuple, Tuple))
set_deserializer(default_union_deserializer, (Union, Optional))
set_deserializer(default_defaultdict_deserializer, DefaultDict)
set_deserializer(default_enum_deserializer, Enum)
set_deserializer(default_datetime_deserializer, datetime)
set_deserializer(default_date_deserializer, date)
set_deserializer(default_time_deserializer, time)
set_deserializer(default_timezone_deserializer, timezone)
set_deserializer(default_timedelta_deserializer, timedelta)
set_deserializer(default_string_deserializer, str)
set_deserializer(default_nonetype_deserializer, NoneType)
set_deserializer(default_primitive_deserializer, (int, float, bool))
set_deserializer(default_mapping_deserializer, (Mapping, dict, Dict), False)
set_deserializer(default_iterable_deserializer, Iterable, False)
set_deserializer(default_object_deserializer, object, False)
set_deserializer(default_uuid_deserializer, UUID)
set_deserializer(default_complex_deserializer, complex)
set_deserializer(default_decimal_deserializer, Decimal)
set_deserializer(default_path_deserializer, PurePath)

if default_zone_info_serializer and default_zone_info_deserializer:
    from zoneinfo import ZoneInfo
    __all__.append(default_zone_info_serializer)
    __all__.append(default_zone_info_deserializer)
    set_serializer(default_zone_info_serializer, ZoneInfo)
    set_deserializer(default_zone_info_deserializer, ZoneInfo)
