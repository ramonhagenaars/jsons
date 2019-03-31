from unittest import TestCase, skipUnless
import jsons

try:
    from dataclasses import dataclass
except ImportError:
    dataclass = None


class TestSpecificVersions(TestCase):

    @skipUnless(dataclass, reason='Only 3.7+')
    def test_simple_dump_and_load_dataclass(self):
        from tests.python37 import Person
        p = Person('John')
        dumped = jsons.dump(p)
        loaded = jsons.load(dumped, Person)
        self.assertEqual(p.name, loaded.name)
