"""
This package contains default serializers. You can override the
serialization process of a particular type as follows:

``jsons.set_serializer(custom_serializer, SomeClass)``
"""
from jsons._key_transformers import snakecase, camelcase, pascalcase, lispcase
from jsons.serializers.default_datetime import default_datetime_serializer
from jsons.serializers.default_date import default_date_serializer
from jsons.serializers.default_time import default_time_serializer
from jsons.serializers.default_timezone import default_timezone_serializer
from jsons.serializers.default_timedelta import default_timedelta_serializer
from jsons.serializers.default_dict import default_dict_serializer
from jsons.serializers.default_enum import default_enum_serializer
from jsons.serializers.default_iterable import default_iterable_serializer
from jsons.serializers.default_object import default_object_serializer
from jsons.serializers.default_primitive import default_primitive_serializer
from jsons.serializers.default_tuple import default_tuple_serializer
from jsons.serializers.default_uuid import default_uuid_serializer


KEY_TRANSFORMER_SNAKECASE = snakecase
KEY_TRANSFORMER_CAMELCASE = camelcase
KEY_TRANSFORMER_PASCALCASE = pascalcase
KEY_TRANSFORMER_LISPCASE = lispcase
