import datetime
from unittest import TestCase
import jsons


class TestList(TestCase):
    def test_dump_list(self):
        d = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                              tzinfo=datetime.timezone.utc)
        l = [1, 2, 3, [4, 5, [d]]]
        self.assertEqual([1, 2, 3, [4, 5, ['2018-07-08T21:34:00Z']]],
                         jsons.dump(l))

    def test_load_list(self):
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        list_ = [1, 2, 3, [4, 5, [dat]]]
        expectation = [1, 2, 3, [4, 5, ['2018-07-08T21:34:00Z']]]
        self.assertEqual(list_, jsons.load(expectation))
