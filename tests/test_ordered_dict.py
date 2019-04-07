from collections import OrderedDict
from unittest import TestCase
import jsons


class TestOrderedDict(TestCase):
    def test_dump_ordered_dict(self):
        d = {
            'a': 'A',
            'b': 'B'
        }
        od = OrderedDict(d)
        dumped = jsons.dump(od)
        self.assertDictEqual(d, dumped)

    def test_load_ordered_dict(self):
        d = {
            'a': 'A',
            'b': 'B'
        }
        loaded = jsons.load(d, OrderedDict)
        self.assertDictEqual(OrderedDict(d), loaded)
