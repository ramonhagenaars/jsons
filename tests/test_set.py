import datetime
from typing import Set
from unittest import TestCase
import jsons


class TestSet(TestCase):
    def test_dump_set(self):
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        set_ = {dat, dat}
        dumped = jsons.dump(set_)
        expected = ['2018-07-08T21:34:00Z']
        self.assertEqual(dumped, expected)

    def test_load_set(self):
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        loaded1 = jsons.load(['2018-07-08T21:34:00Z'], set)
        loaded2 = jsons.load(['2018-07-08T21:34:00Z'], Set[str])
        self.assertEqual(loaded1, {dat})
        self.assertEqual(loaded2, {'2018-07-08T21:34:00Z'})
