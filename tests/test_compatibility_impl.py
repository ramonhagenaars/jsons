from unittest import TestCase

from jsons._compatibility_impl import Flag


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
