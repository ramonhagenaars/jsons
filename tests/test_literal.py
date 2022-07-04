import enum
from typing import Literal, List, Union
from unittest import TestCase

import jsons
from jsons import DeserializationError


class TestUnion(TestCase):
    def test_dump_literal(self):
        class A:
            def __init__(self, x: Literal[5]):
                self.x = x
        expected = {'x': 5}
        dumped = jsons.dump(A(5))
        
        self.assertDictEqual(expected, dumped)

    def test_load_literal(self):
        class A:
            def __init__(self, x: Literal['one', 'two']):
                self.x = x

        self.assertEqual('one', jsons.load({'x': 'one'}, A).x)
        self.assertEqual('two', jsons.load({'x': 'two'}, A).x)

        with self.assertRaises(DeserializationError):
            jsons.load({'x': 'does not match the literal'}, A).x

    def test_load_strictly_equal_literal(self):
        class ExType(enum.IntEnum):
            FIRST = 1
            SECOND = 2

        class A:
            def __init__(self, x: Literal[ExType.FIRST]):
                self.x = x

        class B:
            def __init__(self, x: Literal[1]):
                self.x = x

        self.assertEqual(ExType.FIRST, jsons.load({'x': 1}, A).x)
        self.assertEqual(1, jsons.load({'x': 1}, B).x)
        with self.assertRaises(DeserializationError):
            jsons.load({'x': 1}, A, strictly_equal_literal=True)

    def test_load_literal_disambiguates_unions(self):
        class A:
            def __init__(self, a: int, b: Literal[1]):
                self.a = a
                self.b = b
        class B:
            def __init__(self, a: int, b: Literal[2]):
                self.a = a
                self.b = b

        col = jsons.load([{"a": 0, "b": 2}, {"a": 5, "b": 1}, {"a": 0, "b": 2}, {"a": 3, "b": 1}], List[Union[A, B]])
        self.assertIsInstance(col[0], B)
        self.assertIsInstance(col[1], A)
        self.assertIsInstance(col[2], B)
        self.assertIsInstance(col[3], A)
