from unittest import TestCase
from jsons import Verbosity


class TestVerbosity(TestCase):
    def test_verbosity_from_value(self):
        self.assertEqual(Verbosity.WITH_DUMP_TIME, Verbosity.from_value(Verbosity.WITH_DUMP_TIME))
        self.assertEqual(Verbosity.WITH_NOTHING, Verbosity.from_value(False))
        self.assertEqual(Verbosity.WITH_NOTHING, Verbosity.from_value(None))
        self.assertEqual(Verbosity.WITH_EVERYTHING, Verbosity.from_value(True))
        self.assertEqual(Verbosity.WITH_EVERYTHING, Verbosity.from_value([1, 2, 3]))
