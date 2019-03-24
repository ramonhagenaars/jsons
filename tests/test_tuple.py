import datetime
from collections import namedtuple
from typing import NamedTuple, Tuple, List
from unittest import TestCase
import jsons
from jsons import UnfulfilledArgumentError


class TestTuple(TestCase):
    def test_dump_tuple(self):
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        tup = (1, 2, 3, [4, 5, (dat,)])
        self.assertEqual([1, 2, 3, [4, 5, ['2018-07-08T21:34:00Z']]],
                         jsons.dump(tup))

    def test_dump_namedtuple(self):
        T = namedtuple('T', ['x', 'y'])
        t = T(1, 2)
        dumped = jsons.dump(t)
        self.assertDictEqual({'x': 1, 'y': 2}, dumped)

        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        T2 = NamedTuple('T2', [('x', str), ('y', datetime.datetime)])
        t2 = T2('test', dat)
        dumped2 = jsons.dump(t2)
        self.assertDictEqual({'x': 'test', 'y': '2018-07-08T21:34:00Z'}, dumped2)

    def test_dump_namedtuple_with_types(self):
        A = NamedTuple('A', [('x', str), ('y', datetime.datetime)])
        B = NamedTuple('B', [('a', A)])

        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        b = B(A('test', dat))

        expectation = {'a': {'x': 'test', 'y': '2018-07-08T21:34:00Z'}}
        dumped = jsons.dump(b)

        self.assertDictEqual(expectation, dumped)

    def test_load_tuple(self):
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        tup = (1, ([dat],))
        expectation = (1, (['2018-07-08T21:34:00Z'],))
        cls = Tuple[int, Tuple[List[datetime.datetime]]]
        self.assertEqual(tup, jsons.load(expectation, cls))

    def test_load_namedtuple_with_types(self):
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        T = NamedTuple('T', [('x', str), ('y', datetime.datetime)])
        t = T('test', dat)

        loaded_from_list = jsons.load(['test', '2018-07-08T21:34:00Z'], T)
        loaded_from_dict = jsons.load({'x': 'test', 'y': '2018-07-08T21:34:00Z'}, T)

        self.assertEqual(t, loaded_from_list)
        self.assertEqual(t, loaded_from_dict)

        T._field_defaults = dict(y=dat)

        loaded_from_list2 = jsons.load(['test'], T)
        loaded_from_dict2 = jsons.load({'x': 'test'}, T)

        self.assertEqual(t, loaded_from_list2)
        self.assertEqual(t, loaded_from_dict2)

        with self.assertRaises(UnfulfilledArgumentError):
            jsons.load([], T)
        try:
            jsons.load([], T)
        except UnfulfilledArgumentError as err:
            self.assertEqual([], err.source)
            self.assertEqual(T, err.target)
            self.assertEqual('x', err.argument)

        with self.assertRaises(UnfulfilledArgumentError):
            jsons.load({}, T)
        try:
            jsons.load({}, T)
        except UnfulfilledArgumentError as err:
            self.assertEqual({}, err.source)
            self.assertEqual(T, err.target)
            self.assertEqual('x', err.argument)

    def test_load_namedtuple_without_types(self):
        T = namedtuple('T', ['x', 'y'])

        loaded_from_list = jsons.load(['100', 200], T)
        loaded_from_dict = jsons.load({'x': '100', 'y': 200}, T)

        self.assertEqual('100', loaded_from_list.x)
        self.assertEqual(200, loaded_from_list.y)
        self.assertEqual('100', loaded_from_dict.x)
        self.assertEqual(200, loaded_from_dict.y)

    def test_load_namedtuple_with_empty(self):
        T = namedtuple('T', ['x', 'y'])

        loaded_from_list = jsons.load(['', ''], T)
        loaded_from_dict = jsons.load({'x': '', 'y': ''}, T)

        self.assertEqual('', loaded_from_list.x)
        self.assertEqual('', loaded_from_list.y)
        self.assertEqual('', loaded_from_dict.x)
        self.assertEqual('', loaded_from_dict.y)

    def test_load_tuple_with_n_length(self):
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        expectation = (dat, dat)

        loaded = jsons.load(['2018-07-08T21:34:00Z',
                             '2018-07-08T21:34:00Z'],
                            cls=Tuple[datetime.datetime, ...])

        self.assertEqual(expectation, loaded)
