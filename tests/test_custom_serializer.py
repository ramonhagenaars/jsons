from unittest import TestCase
import jsons
from jsons import default_string_deserializer, default_primitive_serializer


class TestCustomSerializer(TestCase):
    def test_set_custom_functions(self):
        jsons.set_serializer(lambda *_, **__: 'custom_serializer', str)
        jsons.set_deserializer(lambda *_, **__: 'custom_deserializer', str)

        dumped = jsons.dump('serialize me')
        loaded = jsons.load(dumped)

        self.assertEqual(dumped, 'custom_serializer')
        self.assertEqual(loaded, 'custom_deserializer')

    @classmethod
    def tearDownClass(cls):
        jsons.set_serializer(default_primitive_serializer, str)
        jsons.set_deserializer(default_string_deserializer, str)
