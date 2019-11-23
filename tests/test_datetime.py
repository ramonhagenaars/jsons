import datetime
import warnings
from unittest import TestCase
import jsons
from jsons._common_impl import StateHolder
from jsons._datetime_impl import get_offset_str


class TestDatetime(TestCase):
    def test_dump_naive_datetime(self):
        d = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34)
        dumped = jsons.dump(d)
        self.assertTrue(dumped.startswith('2018-07-08T21:34:00'))
        self.assertTrue(not dumped.endswith('Z'))

    def test_dump_datetime_utcnow(self):
        d = datetime.datetime.utcnow()
        dumped = jsons.dump(d)
        # utcnow generates a datetime without tzinfo.
        self.assertTrue(not dumped.endswith('Z'))

    def test_dump_datetime_with_tzinfo(self):
        d = datetime.datetime.now(datetime.timezone.utc)
        dumped = jsons.dump(d)
        # utcnow generates a datetime without tzinfo.
        self.assertTrue(dumped.endswith('Z'))

    def test_dump_datetime_without_tz(self):
        # By default, naive datetimes trigger a warning.
        with warnings.catch_warnings(record=True) as w:
            jsons.dump(datetime.datetime.now())
            self.assertEqual(1, len(w))
            self.assertTrue(issubclass(w[0].category, UserWarning))

        jsons.suppress_warnings()

        # Warnings are now suppressed.
        with warnings.catch_warnings(record=True) as w:
            jsons.dump(datetime.datetime.now())
            self.assertEqual(0, len(w))

        jsons.suppress_warnings(False)

        # The warnings are back on now.
        with warnings.catch_warnings(record=True) as w:
            jsons.dump(datetime.datetime.now())
            self.assertEqual(1, len(w))
            self.assertTrue(issubclass(w[0].category, UserWarning))

    def test_dump_datetime_with_stripped_microseconds(self):
        d = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                              second=10, microsecond=123456,
                              tzinfo=datetime.timezone.utc)
        dumped = jsons.dump(d)
        self.assertEqual('2018-07-08T21:34:10Z', dumped)

    def test_dump_datetime_with_microseconds(self):
        d = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                              microsecond=123456, tzinfo=datetime.timezone.utc)
        dumped = jsons.dump(d, strip_microseconds=False)
        self.assertEqual('2018-07-08T21:34:00.123456Z', dumped)

    def test_dump_datetime_with_tz(self):
        tzinfo = datetime.timezone(datetime.timedelta(hours=-2))
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=tzinfo)
        dumped = jsons.dump(dat)
        self.assertEqual(dumped, '2018-07-08T21:34:00-02:00')

    def test_load_datetime(self):
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        self.assertEqual(dat, jsons.load('2018-07-08T21:34:00Z'))

    def test_load_datetime_with_ms(self):
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                second=0,microsecond=123456,
                                tzinfo=datetime.timezone.utc)
        self.assertEqual(dat, jsons.load('2018-07-08T21:34:00.123456Z'))

    def test_load_datetime_with_tz(self):
        tzinfo = datetime.timezone(datetime.timedelta(hours=-2))
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=tzinfo)
        loaded = jsons.load('2018-07-08T21:34:00-02:00')
        self.assertEqual(loaded, dat)

    def test_get_offset_str(self):
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)

        td = datetime.timedelta(hours=3)

        dat2 = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone(td))

        offset_str_dat = get_offset_str(dat, StateHolder)
        offset_str_dat2 = get_offset_str(dat2, StateHolder)
        offset_str_td = get_offset_str(td, StateHolder)

        self.assertEqual('Z', offset_str_dat)
        self.assertEqual('+03:00', offset_str_dat2)
        self.assertEqual('+03:00', offset_str_td)
