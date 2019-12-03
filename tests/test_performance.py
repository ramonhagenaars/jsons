from datetime import datetime
from typing import List
from unittest import TestCase

import jsons


class C1:
    def __init__(self, x: int, y: str):
        self.x = x
        self.y = y


class C2:
    def __init__(self, list_of_c1: List[C1]):
        self.list_of_c1 = list_of_c1


class C3:
    def __init__(self, list_of_c2: List[C2]):
        self.list_of_c2 = list_of_c2


class TestPerformance(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._c3_1 = None
        self._c3_2 = None
        self._c3_3 = None

    @classmethod
    def setUpClass(cls) -> None:
        cls._c3_1 = cls._create_c3(100, 10)
        cls._c3_2 = cls._create_c3(100, 100)
        cls._c3_3 = cls._create_c3(100, 1000)

    @staticmethod
    def _create_c3(len1: int, len2: int) -> C3:
        list_of_c1 = [C1(x, str(x)) for x in range(len1)]
        list_of_c2 = [C2(list_of_c1) for _ in range(len2)]
        return C3(list_of_c2)

    def test_dump(self):
        self._do_test_dump(16)

    def test_dump_strict(self):
        self._do_test_dump(8, strict=True)

    def _do_test_dump(self, time_limit: int, **kwargs):
        d1 = datetime.now()
        jsons.dump(self.__class__._c3_1, **kwargs)
        d2 = datetime.now()

        d3 = datetime.now()
        jsons.dump(self.__class__._c3_2, **kwargs)
        d4 = datetime.now()

        d5 = datetime.now()
        jsons.dump(self.__class__._c3_3, **kwargs)
        d6 = datetime.now()

        delta_sec1 = float('{}.{}'.format((d2 - d1).seconds, (d2 - d1).microseconds))
        delta_sec2 = float('{}.{}'.format((d4 - d3).seconds, (d4 - d3).microseconds))
        delta_sec3 = float('{}.{}'.format((d6 - d5).seconds, (d6 - d5).microseconds))

        self.assertTrue(delta_sec3 < time_limit, 'The operation took {} seconds'.format(delta_sec3))
        threshold = 0.1
        avg1 = delta_sec1 / 10
        avg2 = delta_sec2 / 100
        avg3 = delta_sec3 / 1000
        linear_scaling = abs(avg2 - avg1) < threshold and abs(avg3 - avg2) < threshold

        self.assertTrue(linear_scaling, '{}, {}'.format(abs(avg2 - avg1), abs(avg3 - avg2)))
