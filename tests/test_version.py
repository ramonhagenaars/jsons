from unittest import TestCase


class TestVersion(TestCase):
    def test_version(self):
        # Test that __version__ can be imported from jsons
        from jsons import __version__

        # Test that __version__ consists of major.minor.patch
        self.assertEqual(3, len(__version__.split('.')))
