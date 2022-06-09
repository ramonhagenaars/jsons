from datetime import datetime
from unittest import TestCase

import jsons


class TestStr(TestCase):
    def test_string_is_loaded_as_string(self):

        class C:
            def __init__(self, x: str):
                self.x = x

        fork = jsons.fork()
        jsons.set_deserializer(lambda obj, _, **kwargs: datetime.strptime(obj, '%Y'), datetime, fork_inst=fork)
        loaded = jsons.load({'x': '1025'}, C, strict=True, fork_inst=fork)

        self.assertIsInstance(loaded.x, str)

    def test_string_is_loaded_as_datetime(self):

        class C:
            def __init__(self, x):
                # x has no hint, so the type will be inferred. Since x is not
                # explicitly targeted as str, it may get parsed as a datetime.
                # And in this test, it should.
                self.x = x

        fork = jsons.fork()
        jsons.set_deserializer(lambda obj, _, **kwargs: datetime.strptime(obj, '%Y'), datetime, fork_inst=fork)
        loaded = jsons.load({'x': '1025'}, C, strict=True, fork_inst=fork)

        self.assertIsInstance(loaded.x, datetime)
