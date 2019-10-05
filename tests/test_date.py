from datetime import datetime, date
from unittest import TestCase
import jsons


class TestDate(TestCase):
    def test_dump_date(self):
        d = datetime(year=2018, month=7, day=8, hour=21, minute=34).date()
        dumped = jsons.dump(d)
        self.assertEqual('2018-07-08', dumped)

    def test_load_date(self):
        loaded = jsons.load('2018-07-08', date)

        expected = datetime(year=2018, month=7, day=8, hour=21, minute=34).date()
        self.assertEqual(expected, loaded)
