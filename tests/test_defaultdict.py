from collections import defaultdict
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
