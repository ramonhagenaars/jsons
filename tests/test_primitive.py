from datetime import datetime
from unittest import TestCase
import jsons
from jsons import DeserializationError


class TestPrimitive(TestCase):

    def test_dump_str(self):
        self.assertEqual('some string', jsons.dump('some string'))

    def test_dump_int(self):
        self.assertEqual(123, jsons.dump(123))

    def test_dump_float(self):
        self.assertEqual(123.456, jsons.dump(123.456))

    def test_dump_bool(self):
        self.assertEqual(True, jsons.dump(True))

    def test_dump_none(self):
        self.assertEqual(None, jsons.dump(None))

    def test_load_str(self):
        self.assertEqual('some string', jsons.load('some string'))

    def test_load_int(self):
        self.assertEqual(123, jsons.load(123))

    def test_load_float(self):
        self.assertEqual(123.456, jsons.load(123.456))

    def test_load_bool(self):
        self.assertEqual(True, jsons.load(True))

    def test_load_and_cast(self):

        class C:
            def __init__(self, x: int):
                self.x = x

        self.assertEqual(42, jsons.load('42', int))
        self.assertEqual(42.0, jsons.load('42', float))
        self.assertEqual('42', jsons.load(42, str))
        self.assertEqual(True, jsons.load(42, bool))

        with self.assertRaises(DeserializationError):
            jsons.load('fortytwo', int)

        try:
            jsons.load('fortytwo', int)
        except DeserializationError as err:
            self.assertEqual('fortytwo', err.source)
            self.assertEqual(int, err.target)
