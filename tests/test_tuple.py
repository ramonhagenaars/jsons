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
        self.assertEqual([1, 2], dumped)

        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        T2 = NamedTuple('T2', [('x', str), ('y', datetime.datetime)])
        t2 = T2('test', dat)
        dumped2 = jsons.dump(t2)
        self.assertEqual(['test', '2018-07-08T21:34:00Z'], dumped2)

    def test_load_tuple(self):
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        tup = (1, ([dat],))
        expectation = (1, (['2018-07-08T21:34:00Z'],))
        cls = Tuple[int, Tuple[List[datetime.datetime]]]
        self.assertEqual(tup, jsons.load(expectation, cls))

    def test_load_namedtuple(self):
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        T = NamedTuple('T', [('x', str), ('y', datetime.datetime)])
        t = T('test', dat)
        loaded = jsons.load(['test', '2018-07-08T21:34:00Z'], T)
        self.assertEqual(t, loaded)

        T._field_defaults = dict(y=dat)
        loaded2 = jsons.load(['test'], T)
        self.assertEqual(t, loaded)

        with self.assertRaises(UnfulfilledArgumentError):
            jsons.load([], T)
        try:
            jsons.load([], T)
        except UnfulfilledArgumentError as err:
            self.assertEqual([], err.source)
            self.assertEqual(T, err.target)
            self.assertEqual('x', err.argument)

    def test_load_namedtuple_without_types(self):
        T = namedtuple('T', ['x', 'y'])
        loaded = jsons.load(['100', 200], T)
        self.assertEqual('100', loaded.x)
        self.assertEqual(200, loaded.y)

    def test_load_namedtuple_with_empty(self):
        T = namedtuple('T', ['x', 'y'])
        loaded = jsons.load(['', ''], T)
        self.assertEqual('', loaded.x)
        self.assertEqual('', loaded.y)

    def test_load_tuple_with_n_length(self):
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        expectation = (dat, dat)
        loaded = jsons.load(['2018-07-08T21:34:00Z',
                             '2018-07-08T21:34:00Z'],
                            cls=Tuple[datetime.datetime, ...])
        self.assertEqual(expectation, loaded)
