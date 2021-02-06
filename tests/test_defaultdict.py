from collections import defaultdict
from typing import DefaultDict
from unittest import TestCase

import jsons


class TestDefaultdict(TestCase):
    def test_dump_defaultdict(self):
        d = {
            'a': 'A',
            'b': 'B'
        }
        dd = defaultdict(list, d)
        dumped = jsons.dump(dd)
        self.assertDictEqual(d, dumped)

    def test_load_defaultdict(self):
        d = {
            'a': [1, 2, 3],
        }
        dd = defaultdict(list, d)

        loaded = jsons.load(d, DefaultDict[str, list])

        self.assertDictEqual(dd, loaded)
        self.assertIsInstance(loaded, defaultdict)
        self.assertEqual(list, loaded.default_factory)

    def test_load_default_dict_without_args(self):
        d = {
            'a': [1, 2, 3],
        }

        dd = defaultdict(None, d)

        loaded = jsons.load(d, DefaultDict)

        self.assertEqual(dd.default_factory, loaded.default_factory)
