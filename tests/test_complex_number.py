from unittest import TestCase
import jsons
from jsons import DeserializationError


class TestComplexNumber(TestCase):
    def test_dump_complex_number(self):
        a = 5 + 3j
        dumped = jsons.dump(a)
        self.assertDictEqual(dumped, {'real': 5.0, 'imag': 3.0})

    def test_dump_complex_number_property(self):
        class A:
            b = 2 + 4j

        dumped = jsons.dump(A())
        self.assertDictEqual(dumped, {'b': {'real': 2.0, 'imag': 4.0}})

    def test_load_complex_number(self):
        dumped = {'real': 1.0, 'imag': 2.0}
        loaded = jsons.load(dumped, complex)
        self.assertEqual(loaded, 1+2j)

        bad_keys_dump = {'some_key': 3.0}
        with self.assertRaises(DeserializationError):
            jsons.load(bad_keys_dump, complex)

        bad_types_dump = {'real': 'some_string', 'imag': {'a': 2}}
        with self.assertRaises(DeserializationError):
            jsons.load(bad_types_dump, complex)
