import datetime
from multiprocessing import Process
from threading import Thread
from typing import List
from unittest import TestCase

import jsons
from jsons import _multitasking, DeserializationError
from jsons.exceptions import JsonsError


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

    def test_dump_list_strict_no_cls(self):
        class C:
            def __init__(self, x: int, y: str):
                self.x = x
                self.y = y

        l = [C(1, '2')] * 5
        expected = [{'x': 1, 'y': '2'}] * 5
        dumped = jsons.dump(l, strict=True)
        self.assertListEqual(expected, dumped)

    # Note: mock.patch won't work because of a subclass check.
    def test_dump_list_multiprocess(self):

        class ProcessMock(Process):
            def __init__(self, target, args, *_, **__):
                # Make no super call.
                self.target = target
                self.args = args

            def start(self):
                return self.target(*self.args)

            def join(self, *_, **__) -> None:
                pass

        class ManagerMock:
            def list(self, l, *_, **__):
                return l

        jsons._multitasking.Manager = ManagerMock

        dumped = jsons.dump(['1', '1', '1', '1'], List[int], strict=True,
                            tasks=2, task_type=ProcessMock)
        self.assertEqual([1, 1, 1, 1], dumped)

    def test_load_list(self):
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        expectation = [1, 2, 3, [4, 5, [dat]]]

        loaded = jsons.load([1, 2, 3, [4, 5, ['2018-07-08T21:34:00Z']]])

        self.assertEqual(expectation, loaded)

    def test_load_list_typing(self):
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        expectation = [1, 2, 3, [4, 5, [dat]]]

        loaded = jsons.load([1, 2, 3, [4, 5, ['2018-07-08T21:34:00Z']]], List)

        self.assertEqual(expectation, loaded)

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
        self.assertEqual(list_, jsons.load(expectation, tasks=3,
                                           task_type=Thread))

        with self.assertRaises(JsonsError):
            jsons.load(expectation, tasks=-1,
                       task_type=Thread)

        self.assertEqual([1], jsons.load(['1'], List[int], tasks=2,
                                         task_type=Thread))

        # More tasks than elements should still work.
        self.assertEqual([1, 1, 1, 1], jsons.load(['1', '1', '1', '1'],
                                                  List[int], tasks=16,
                                                  task_type=Thread))

    # Note: mock.patch won't work because of a subclass check.
    def test_load_list_multiprocess(self):

        class ProcessMock(Process):
            def __init__(self, target, args, *_, **__):
                # Make no super call.
                self.target = target
                self.args = args

            def start(self):
                return self.target(*self.args)

            def join(self, *_, **__) -> None:
                pass

        class ManagerMock:
            def list(self, l, *_, **__):
                return l

        jsons._multitasking.Manager = ManagerMock

        self.assertEqual([1, 1, 1, 1], jsons.load(['1', '1', '1', '1'],
                                                  List[int], tasks=2,
                                                  task_type=ProcessMock))

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

    def test_load_error_points_at_index(self):

        class C:
            def __init__(self, x: str, y: int):
                self.x = x
                self.y = y

        c_objs_dict = [{'x': str(i), 'y': i} for i in range(1000)]
        c_objs_dict[500] = {'not_x': '42', 'y': 42}

        with self.assertRaises(DeserializationError) as err:
            jsons.load(c_objs_dict, List[C])

        self.assertIn('500', str(err.exception))
