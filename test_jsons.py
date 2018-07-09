from enum import Enum
from typing import List
from unittest.case import TestCase
import datetime
import jsons


class TestJsons(TestCase):

    def test_dump_str(self):
        self.assertEqual('some string', jsons.dump('some string'))

    def test_dump_int(self):
        self.assertEqual(123, jsons.dump(123))

    def test_dump_float(self):
        self.assertEqual(123.456, jsons.dump(123.456))

    def test_dump_bool(self):
        self.assertEqual(True, jsons.dump(True))

    def test_dump_dict(self):
        self.assertEqual({'a': 123}, jsons.dump({'a': 123}))

    def test_dump_none(self):
        self.assertEqual(None, jsons.dump(None))

    def test_dump_datetime(self):
        d = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34)
        self.assertEqual('2018-07-08T21:34:00Z', jsons.dump(d))

    def test_dump_enum(self):
        class E(Enum):
            x = 1
            y = 2
        self.assertEqual('x', jsons.dump(E.x))

    def test_dump_list(self):
        d = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34)
        l = [1, 2, 3, [4, 5, [d]]]
        self.assertEqual([1, 2, 3, [4, 5, ['2018-07-08T21:34:00Z']]], jsons.dump(l))

    def test_dump_object(self):
        class A:
            def __init__(self):
                self.name = 'A'

        class B:
            def __init__(self, a):
                self.a = a
                self.name = 'B'

        b = B(A())
        self.assertEqual({'name': 'B', 'a': {'name': 'A'}}, jsons.dump(b))

    def test_load_str(self):
        self.assertEqual('some string', jsons.load('some string'))

    def test_load_int(self):
        self.assertEqual(123, jsons.load(123))

    def test_load_float(self):
        self.assertEqual(123.456, jsons.load(123.456))

    def test_load_bool(self):
        self.assertEqual(True, jsons.load(True))

    def test_load_dict(self):
        self.assertEqual({'a': 123}, jsons.load({'a': 123}))

    def test_load_none(self):
        self.assertEqual(None, jsons.load(None))

    def test_load_datetime(self):
        d = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34)
        self.assertEqual(d, jsons.load('2018-07-08T21:34:00Z'))

    def test_load_enum(self):
        class E(Enum):
            x = 1
            y = 2

        self.assertEqual(E.x, jsons.load('x', E))

    def test_load_list(self):
        d = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34)
        l = [1, 2, 3, [4, 5, [d]]]
        self.assertEqual(l, jsons.load([1, 2, 3, [4, 5, ['2018-07-08T21:34:00Z']]]))

    def test_load_object(self):
        class A:
            def __init__(self):
                self.name = 'A'

        class B:
            def __init__(self, a: A):
                self.a = a
                self.name = 'B'

        b = B(A())
        loaded_b = jsons.load({'name': 'B', 'a': {'name': 'A'}}, B)
        self.assertEqual(b.name, loaded_b.name)
        self.assertEqual(b.a.name, loaded_b.a.name)

    def test_load_object_with_default_value(self):
        class A:
            def __init__(self, x, y = 2):
                self.x = x
                self.y = y

        a = A(1)
        loaded_a = jsons.load({'x': 1}, A)
        self.assertEqual(a.x, loaded_a.x)
        self.assertEqual(a.y, loaded_a.y)

    def test_dump_load_object_deep(self):
        class A:
            def __init__(self):
                self.name = 'A'

        class B:
            def __init__(self, list_a: List[A], list_dates: List[datetime.datetime]):
                self.list_a = list_a
                self.list_dates = list_dates
                self.name = 'B'

        class C:
            def __init__(self, list_b: List[B]):
                self.list_b = list_b

        c = C([B([A(), A()], []), B([], [datetime.datetime.now(), datetime.datetime.now()])])
        dumped_c = jsons.dump(c)
        loaded_c = jsons.load(dumped_c, C)
        self.assertEqual(loaded_c.list_b[0].name, 'B')
        self.assertEqual(loaded_c.list_b[0].list_a[0].name, 'A')
        self.assertEqual(loaded_c.list_b[0].list_a[1].name, 'A')
        self.assertEqual(loaded_c.list_b[1].list_dates[0].year, c.list_b[1].list_dates[0].year)
        self.assertEqual(loaded_c.list_b[1].list_dates[0].month, c.list_b[1].list_dates[0].month)
        self.assertEqual(loaded_c.list_b[1].list_dates[0].day, c.list_b[1].list_dates[0].day)
        self.assertEqual(loaded_c.list_b[1].list_dates[0].hour, c.list_b[1].list_dates[0].hour)
        self.assertEqual(loaded_c.list_b[1].list_dates[0].minute, c.list_b[1].list_dates[0].minute)
        self.assertEqual(loaded_c.list_b[1].list_dates[0].second, c.list_b[1].list_dates[0].second)
