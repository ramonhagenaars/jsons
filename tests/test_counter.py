from collections import Counter
from unittest import TestCase
import jsons


class TestCounter(TestCase):
    def test_dump_counter(self):
        c = Counter('A counter is something that counts!')
        dumped = jsons.dump(c)
        expected = {
            'A': 1,
            ' ': 5,
            'c': 2,
            'o': 3,
            'u': 2,
            'n': 3,
            't': 5,
            'e': 2,
            'r': 1,
            'i': 2,
            's': 3,
            'm': 1,
            'h': 2,
            'g': 1,
            'a': 1,
            '!': 1
        }
        self.assertDictEqual(expected, dumped)

    def test_load_counter(self):
        d = {
            'A': 1,
            ' ': 5,
            'c': 2,
            'o': 3,
            'u': 2,
            'n': 3,
            't': 5,
            'e': 2,
            'r': 1,
            'i': 2,
            's': 3,
            'm': 1,
            'h': 2,
            'g': 1,
            'a': 1,
            '!': 1
        }
        loaded = jsons.load(d, Counter)
        self.assertEqual(Counter(d), Counter(loaded))
