import sys
import typing
from unittest import TestCase
from unittest.mock import MagicMock

from jsons._compatibility_impl import Flag, get_type_hints


class TestCompatibilityImpl(TestCase):
    def test_flag(self):

        class F(Flag):
            A = 0
            B = 10
            C = 20
            D = 40
            E = 80

        self.assertEqual(20, F.C.value)
        self.assertEqual(30, (F.B | F.C).value)
        self.assertTrue(F.A in (F.B | F.C))
        self.assertTrue(F.B in (F.B | F.C))
        self.assertTrue(F.C in (F.B | F.C))
        self.assertTrue(F.D not in (F.B | F.C))
        self.assertTrue(F.C not in (F.B | F.D))
        self.assertTrue(F.E not in (F.B | F.D))

    def test_get_type_hints(self):

        def get_type_hints_mock(_, globalns=None):
            if not globalns:
                raise NameError()
            get_type_hints_mock.globalns = globalns
            return {}

        orig = typing.get_type_hints

        try:
            typing.get_type_hints = MagicMock(side_effect=AttributeError)
            result = get_type_hints(lambda: 42)
            self.assertEqual({}, result)

            typing.get_type_hints = get_type_hints_mock
            result = get_type_hints(lambda: 42, 'test_compatibility_impl')

            self.assertDictEqual(sys.modules['test_compatibility_impl'].__dict__, get_type_hints_mock.globalns)
            self.assertEqual({}, result)
        finally:
            typing.get_type_hints = orig
