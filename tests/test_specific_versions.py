import sys
from pathlib import Path
from unittest import TestCase, skipUnless
import jsons

try:
    from dataclasses import dataclass
except ImportError:
    dataclass = None


# Load the test resources into the path, so they can be imported. They MUST
# remain outside of the tests package to prevent the test discovery from
# reading in them too soon.
path = Path(__file__).parent.parent.joinpath(Path('test_resources')).absolute()
sys.path.insert(0, str(path))


class TestSpecificVersions(TestCase):

    @skipUnless(dataclass, reason='Only 3.7+')
    def test_simple_dump_and_load_dataclass(self):
        from python37 import Person
        p = Person('John')
        dumped = jsons.dump(p)
        loaded = jsons.load(dumped, Person)
        self.assertEqual(p.name, loaded.name)
