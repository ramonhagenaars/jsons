from enum import Enum, IntEnum
from unittest import TestCase

import jsons
from jsons import DeserializationError


class TestEnum(TestCase):
    def test_dump_enum(self):
        class E(Enum):
            x = 1
            y = 2

        self.assertEqual('x', jsons.dump(E.x))
        self.assertEqual(2, jsons.dump(E.y, use_enum_name=False))

    def test_load_enum(self):
        class E(Enum):
            x = 1
            y = 2

        self.assertEqual(E.y, jsons.load('y', E))
        self.assertEqual(E.y, jsons.load(2, E))
        self.assertEqual(E.y, jsons.load('y', E, use_enum_name=True))
        self.assertEqual(E.y, jsons.load(2, E, use_enum_name=False))
        with self.assertRaises(DeserializationError):
            self.assertEqual(E.y, jsons.load(2, E, use_enum_name=True))
        with self.assertRaises(DeserializationError):
            self.assertEqual(E.y, jsons.load('y', E, use_enum_name=False))

    def test_dump_intenum(self):
        class IE(IntEnum):
            x = 1
            y = 2

        self.assertEqual('x', jsons.dump(IE.x))
        self.assertEqual(2, jsons.dump(IE.y, use_enum_name=False))

    def test_load_intenum(self):
        class IE(IntEnum):
            x = 1
            y = 2

        self.assertEqual(IE.x, jsons.load('x', IE))
        self.assertEqual(IE.y, jsons.load(2, IE))
        self.assertEqual(IE.y, jsons.load('y', IE, use_enum_name=True))
        self.assertEqual(IE.y, jsons.load(2, IE, use_enum_name=False))
        with self.assertRaises(DeserializationError):
            self.assertEqual(IE.y, jsons.load(2, IE, use_enum_name=True))
        with self.assertRaises(DeserializationError):
            self.assertEqual(IE.y, jsons.load('y', IE, use_enum_name=False))

