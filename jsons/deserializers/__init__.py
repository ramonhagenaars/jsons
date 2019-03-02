"""
This package contains default deserializers. You can override the
deserialization process of a particular type as follows:

``jsons.set_deserializer(custom_deserializer, SomeClass)``
"""
from jsons._main_impl import snakecase, camelcase, pascalcase, lispcase
from jsons.deserializers.default_datetime import default_datetime_deserializer
from jsons.deserializers.default_dict import default_dict_deserializer
from jsons.deserializers.default_enum import default_enum_deserializer
from jsons.deserializers.default_list import default_list_deserializer
from jsons.deserializers.default_object import default_object_deserializer
from jsons.deserializers.default_set import default_set_deserializer
from jsons.deserializers.default_string import default_string_deserializer
from jsons.deserializers.default_union import default_union_deserializer
from jsons.deserializers.default_primitive import (
    default_primitive_deserializer
)
from jsons.deserializers.default_tuple import (
    default_tuple_deserializer,
    default_namedtuple_deserializer
)


KEY_TRANSFORMER_SNAKECASE = snakecase
KEY_TRANSFORMER_CAMELCASE = camelcase
KEY_TRANSFORMER_PASCALCASE = pascalcase
KEY_TRANSFORMER_LISPCASE = lispcase
