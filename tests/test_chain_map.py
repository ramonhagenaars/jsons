from collections import ChainMap
from unittest import TestCase

import jsons


class TestChainMap(TestCase):
    def test_dump_chain_map(self):
        d1 = {
            'a': 'A',
            'b': 'B'
        }
        d2 = {
            'c': 'C',
            'd': 'D'
        }
        m = ChainMap(d1, d2)

        dumped = jsons.dump(m)
        self.assertDictEqual({**d1, **d2}, dumped)

    def test_load_chain_map(self):
        d = {
            'a': 'A',
            'b': 'B'
        }

        m = jsons.load(d, ChainMap)
        self.assertEqual(ChainMap(d), m)
