import datetime
import uuid
from typing import Optional, Union
from unittest import TestCase

import jsons
from jsons import (
    SerializationError,
    DeserializationError,
    UnfulfilledArgumentError,
)


class TestUnion(TestCase):
    def test_dump_optional_primitive(self):
        class C:
            def __init__(self, x: Optional[str]):
                self.x = x

        expected = {'x': '42'}
        dumped = jsons.dump(C('42'))

        self.assertDictEqual(expected, dumped)

    def test_dump_optional_uuid(self):
        class C:
            def __init__(self, x: Optional[uuid.UUID]):
                self.x = x

        expected = {'x': '00000000-0000-0000-0000-000000000000'}
        dumped = jsons.dump(C(uuid.UUID(int=0)))

        self.assertDictEqual(expected, dumped)

    def test_dump_optional_class_primitive(self):
        class C:
            def __init__(self, x: Optional[int]):
                self.x = x

        expected = {'x': 42}
        dumped = jsons.dump(C(42))

        self.assertDictEqual(expected, dumped)

        expected2 = {'x': None}
        dumped2 = jsons.dump(C(None))

        self.assertDictEqual(expected2, dumped2)

    def test_dump_optional_class_uuid(self):
        class C:
            def __init__(self, x: Optional[uuid.UUID]):
                self.x = x

        expected = {'x': '00000000-0000-0000-0000-000000000000'}
        dumped = jsons.dump(C(uuid.UUID(int=0)))

        self.assertDictEqual(expected, dumped)

        expected2 = {'x': None}
        dumped2 = jsons.dump(C(None))

        self.assertDictEqual(expected2, dumped2)

    def test_dump_optional(self):
        dumped = jsons.dump(None, Optional[int])
        self.assertEqual(None, dumped)

    def test_dump_union(self):
        class A:
            def __init__(self, x: int):
                self.x = x

        class B:
            def __init__(self, y: int):
                self.y = y

        dumped = jsons.dump(A(1), Union[B, A])
        expected = {'x': 1}
        self.assertDictEqual(expected, dumped)

        dumped2 = jsons.dump(A(1), Union[B, A], strict=True)
        expected2 = {'x': 1}
        self.assertDictEqual(expected2, dumped2)

        with self.assertRaises(SerializationError):
            jsons.dump(A(1), Union[B], strict=True)

    def test_dump_union_syntax(self):
        class A:
            def __init__(self, x: int | float):
                self.x = x

        dumped = jsons.dump(A(1))
        expected = {'x': 1}
        self.assertDictEqual(expected, dumped)

        dumped2 = jsons.dump(A(1), strict=True)
        expected2 = {'x': 1}
        self.assertDictEqual(expected2, dumped2)

        dumped = jsons.dump(A(2.0))
        expected = {'x': 2.0}
        self.assertDictEqual(expected, dumped)

        dumped2 = jsons.dump(A(2.0), strict=True)
        expected2 = {'x': 2.0}
        self.assertDictEqual(expected2, dumped2)

    def test_fail(self):
        with self.assertRaises(SerializationError) as err:
            jsons.dump('nope', Union[int, float])

        self.assertIn('str', str(err.exception))
        self.assertIn('int', str(err.exception))
        self.assertIn('float', str(err.exception))

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

    def test_load_union_syntax(self):
        class A:
            def __init__(self, x: int | float):
                self.x = x

        self.assertEqual(1, jsons.load({'x': 1}, A).x)
        self.assertEqual(2.0, jsons.load({'x': 2.0}, A).x)

        # Test Union with invalid value.
        with self.assertRaises(DeserializationError):
            jsons.load({'x': 'no match in the union'}, A).x

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

    def test_load_optional(self):
        class TestOptionalInt:
            def __init__(self, value: Optional[int]):
                self.value = value

        # This seems fine.
        loaded1 = jsons.load({'value': 42}, cls=TestOptionalInt)
        self.assertEqual(42, loaded1.value)

        # Strings are parsed if possible.
        loaded2 = jsons.load({'value': '42'}, cls=TestOptionalInt)
        self.assertEqual(42, loaded2.value)

        # No value or None will result in None.
        loaded3 = jsons.load({}, cls=TestOptionalInt)
        loaded4 = jsons.load({'value': None}, cls=TestOptionalInt)
        self.assertEqual(None, loaded3.value)
        self.assertEqual(None, loaded4.value)

        # Now this will fail.
        with self.assertRaises(DeserializationError):
            jsons.load({'value': 'not good'}, cls=TestOptionalInt)
