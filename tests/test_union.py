import datetime
from typing import Optional, Union
from unittest import TestCase
import jsons
from jsons import DeserializationError, UnfulfilledArgumentError


class TestUnion(TestCase):
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

        self.assertEqual(1, jsons.load({'x': 1}, B).x)
        self.assertEqual(None, jsons.load({'x': None}, B).x)
        self.assertEqual(1, jsons.load({'x': {'x': 1}}, C).x.x)
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
