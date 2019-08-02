from unittest import TestCase
import jsons


class TestComplexNumber(TestCase):
    def test_dump_complex_number(self):
        a: complex = 5 + 3j
        dumped = jsons.dump(a)
        self.assertDictEqual(dumped, {'real': 5.0, 'imag': 3.0})

    def test_dump_complex_number_property(self):
        class A:
            b: complex = 2 + 4j

        dumped = jsons.dump(A())
        self.assertDictEqual(dumped, {'b': {'real': 2.0, 'imag': 4.0}})

    def test_load_complex_number(self):
        dumped = {'imag': 2.0, 'real': 1.0}
        loaded = jsons.load(dumped, complex)
        self.assertEqual(loaded, 1+2j)
