import datetime
from typing import List
from unittest import TestCase
import jsons


class TestList(TestCase):
    def test_dump_list(self):
        d = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                              tzinfo=datetime.timezone.utc)
        l = [1, 2, 3, [4, 5, [d]]]
        self.assertEqual([1, 2, 3, [4, 5, ['2018-07-08T21:34:00Z']]],
                         jsons.dump(l))

    def test_load_list(self):
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        list_ = [1, 2, 3, [4, 5, [dat]]]
        expectation = [1, 2, 3, [4, 5, ['2018-07-08T21:34:00Z']]]
        self.assertEqual(list_, jsons.load(expectation))

    def test_load_list_with_generic(self):
        class C:
            def __init__(self, x: str, y: int):
                self.x = x
                self.y = y

        expectation = [C('a', 1), C('b', 2)]
        loaded = jsons.load([{'x': 'a', 'y': 1}, {'x': 'b', 'y': 2}], List[C])
        self.assertEqual(expectation[0].x, loaded[0].x)
        self.assertEqual(expectation[0].y, loaded[0].y)
        self.assertEqual(expectation[1].x, loaded[1].x)
        self.assertEqual(expectation[1].y, loaded[1].y)
