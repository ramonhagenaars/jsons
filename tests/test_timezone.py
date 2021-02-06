from datetime import timezone, timedelta
from unittest import TestCase

import jsons


class TestTimeZone(TestCase):
    def test_dump_timezone(self):
        tz1 = timezone(timedelta(hours=1))
        tz2 = timezone(timedelta(hours=1), 'Jsonistan')

        expectation1 = {
            'name': 'UTC+01:00',
            'offset': 3600.0
        }
        expectation2 = {
            'name': 'Jsonistan',
            'offset': 3600.0
        }

        dumped1 = jsons.dump(tz1)
        dumped2 = jsons.dump(tz2)

        self.assertDictEqual(expectation1, dumped1)
        self.assertDictEqual(expectation2, dumped2)

    def test_load_timezone(self):
        tz1 = {
            'name': 'UTC+01:00',
            'offset': 3600.0
        }
        tz2 = {
            'name': 'Jsonistan',
            'offset': 3600.0
        }

        expectation1 = timezone(timedelta(hours=1))
        expectation2 = timezone(timedelta(hours=1), 'Jsonistan')

        loaded1 = jsons.load(tz1, timezone)
        loaded2 = jsons.load(tz2, timezone)

        self.assertEqual(expectation1, loaded1)
        self.assertEqual(expectation2, loaded2)
