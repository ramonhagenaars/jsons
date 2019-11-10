import datetime
from multiprocessing import Process
from threading import Thread
from typing import List, Tuple
from unittest import TestCase
import jsons
from jsons.exceptions import JsonsError, SerializationError


class TestIterable(TestCase):
    def test_dump_list_with_cls(self):

        class A:
            __slots__ = ['a']

            def __init__(self, a):
                self.a = a

        class B(A):
            __slots__ = ['a', 'b']

            def __init__(self, a, b):
                A.__init__(self, a)
                self.b = b

        l = [B(a=1, b=2), B(a=3, b=4)]

        dumped1 = jsons.dump(l, List[A])
        dumped2 = jsons.dump(l, List[B])

        expected1 = [{'a': 1}, {'a': 3}]
        expected2 = [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}]

        self.assertListEqual(expected1, dumped1)
        self.assertListEqual(expected2, dumped2)

    def test_dump_tuple_with_cls(self):
        t = (1, '2', 3, '4')

        dumped = jsons.dump(t, Tuple[int, str, int, int])

        expected = [1, '2', 3, 4]  # Note that the last element is an int.

        self.assertListEqual(expected, dumped)

    def test_dump_tuple_with_invalid_cls(self):
        t = (1, '2', 3, '4')

        with self.assertRaises(SerializationError):
            jsons.dump(t, Tuple[int, str, int])  # Not enough types.
