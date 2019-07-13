import datetime
from multiprocessing import Process
from typing import List
from unittest import TestCase
from jsons.exceptions import JsonsError
import jsons


class TestList(TestCase):
    def test_dump_list(self):
        d = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                              tzinfo=datetime.timezone.utc)
        l = [1, 2, 3, [4, 5, [d]]]
        self.assertEqual([1, 2, 3, [4, 5, ['2018-07-08T21:34:00Z']]],
                         jsons.dump(l))

    def test_dump_load_list_verbose(self):
        class Parent:
            pass

        class Child(Parent):
            pass

        class Store:
            def __init__(self, c2s: List[Parent]):
                self.c2s = c2s

        jsons.announce_class(Parent)
        jsons.announce_class(Child)
        jsons.announce_class(Store)

        s = Store([Child()])
        dumped = jsons.dump(s, verbose=True)
        loaded = jsons.load(dumped)
        self.assertEqual(Child, type(loaded.c2s[0]))

    def test_load_list(self):
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        list_ = [1, 2, 3, [4, 5, [dat]]]
        expectation = [1, 2, 3, [4, 5, ['2018-07-08T21:34:00Z']]]
        self.assertEqual(list_, jsons.load(expectation))

    def test_load_list2(self):
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        list_ = [dat]
        expectation = ['2018-07-08T21:34:00Z']
        self.assertEqual(list_, jsons.load(expectation))

    def test_load_list_multithreaded(self):
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        list_ = [1, 2, 3, [4, 5, [dat]]]
        expectation = [1, 2, 3, [4, 5, ['2018-07-08T21:34:00Z']]]
        self.assertEqual(list_, jsons.load(expectation, tasks=3))

        with self.assertRaises(JsonsError):
            jsons.load(expectation, tasks=-1)

        self.assertEqual([1], jsons.load(['1'], List[int], tasks=2))

        # More tasks than elements should still work.
        self.assertEqual([1, 1, 1, 1], jsons.load(['1', '1', '1', '1'],
                                                  List[int], tasks=16))

        # Changing the task_type.
        self.assertEqual([1, 1, 1, 1], jsons.load(['1', '1', '1', '1'],
                                                  List[int], tasks=16,
                                                  task_type=Process))

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
