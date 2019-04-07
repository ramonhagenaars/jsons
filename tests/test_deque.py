from collections import deque
from unittest import TestCase
import jsons


class TestDeque(TestCase):
    def test_dump_deque(self):
        dumped = jsons.dump(deque([1, 2, 3]))
        self.assertEqual([1, 2, 3], dumped)

    def test_load_deque(self):
        loaded = jsons.load([1, 2, 3], deque)
        self.assertEqual(deque([1, 2, 3]), loaded)
