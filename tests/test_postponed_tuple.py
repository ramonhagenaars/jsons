import datetime
from collections import namedtuple
from typing import Tuple, List
from unittest import TestCase


import jsons
from jsons import UnfulfilledArgumentError
from tests.postponed_tuple import Tuplicitous, Tuplicity


class TestPostponedTuple(TestCase):
    def test_dump_namedtuple(self):
        T = Tuplicitous(a=1, b=2, c=Tuplicity(a=99, b=100))
        dumped = jsons.dump(T)
        self.assertDictEqual({'a': 1, 'b': 2, 'c': {'a': 99, 'b': 100}}, dumped)

    def test_load_namedtuple(self):
        d = {'a': 1, 'b': 2, 'c': {'a': 99, 'b': 100}}

        T = jsons.load(d, Tuplicitous)

        self.assertEqual(T, Tuplicitous(a=1, b=2, c=Tuplicity(a=99, b=100)))

