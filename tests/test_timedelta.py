from datetime import timedelta
from unittest import TestCase

import jsons


class TestTimeDelta(TestCase):
    def test_dump_timedelta(self):
        expectation = 867600.0

        dumped = jsons.dump(timedelta(hours=241))

        self.assertEqual(expectation, dumped)

    def test_load_timedelta(self):
        expectation = timedelta(hours=241)

        loaded = jsons.load(867600.0, timedelta)

        self.assertEqual(expectation, loaded)
