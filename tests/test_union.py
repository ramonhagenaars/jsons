import datetime
from dataclasses import dataclass
from typing import Optional, Union
from unittest import TestCase
import jsons
from jsons import DeserializationError, UnfulfilledArgumentError


class TestUnion(TestCase):
    def test_dump_optional(self):

        class C:
            def __init__(self, x: Optional[str]):
                self.x = x

        expected = {'x': '42'}
        dumped = jsons.dump(C('42'))

        self.assertDictEqual(expected, dumped)

    def test_load_union(self):
        class A:
            def __init__(self, x):
                self.x = x

        class B:
            def __init__(self, x: Optional[int]):
                self.x = x

        class C:
            def __init__(self, x: Union[datetime.datetime, A]):
                self.x = x

        # Test loading with None value without type hint.
        self.assertEqual(None, jsons.load({'x': None}, A).x)

        # Test Optional with a value.
        self.assertEqual(1, jsons.load({'x': 1}, B).x)

        # Test Optional with None value.
        self.assertEqual(None, jsons.load({'x': None}, B).x)

        # Test Optional without value.
        self.assertEqual(None, jsons.load({}, B).x)

        # Test Union with a value.
        self.assertEqual(1, jsons.load({'x': {'x': 1}}, C).x.x)

        # Test Union with invalid value.
        with self.assertRaises(DeserializationError):
            jsons.load({'x': 'no match in the union'}, C).x

    def test_load_none(self):

        class C:
            def __init__(self, x: int, y: Optional[int]):
                self.x = x
                self.y = y

        with self.assertRaises(UnfulfilledArgumentError):
            jsons.load({}, cls=C)

        with self.assertRaises(UnfulfilledArgumentError):
            jsons.load({'y': 1}, cls=C)

        jsons.load({'x': 1, 'y': None}, cls=None)  # Should not raise.
        jsons.load({'x': 1, 'y': None}, cls=None, strict=True)  # Should not raise.
        jsons.load({'x': 1}, cls=None, strict=True)  # Should not raise.
        jsons.load(None)  # Should not raise.
