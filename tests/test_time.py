from datetime import datetime, time
from unittest import TestCase

import jsons


class TestTime(TestCase):
    def test_dump_time(self):
        d = datetime(year=2018, month=7, day=8, hour=21, minute=34).time()
        dumped = jsons.dump(d)
        self.assertEqual('21:34:00', dumped)

    def test_load_time(self):
        loaded = jsons.load('21:34:00', time)

        expected = datetime(year=2018, month=7, day=8, hour=21, minute=34).time()
        self.assertEqual(expected, loaded)
