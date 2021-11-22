from dataclasses import dataclass
from typing import Dict, NamedTuple
from unittest import TestCase

import jsons


class Foo(NamedTuple):
    a: int
    b: int
    c: int


@dataclass
class D:
    a: int
    b: int


class TestDict(TestCase):
    def tearDown(cls):
        jsons.set_serializer(jsons.default_primitive_serializer, Foo)
        jsons.set_deserializer(jsons.default_string_deserializer, Foo)

    def test_dict_hashkey_with_serializer(self):
        def foo_serializer(obj, **kwargs):
            return "{},{},{}".format(obj.a, obj.b, obj.c)

        def foo_deserializer(obj, cls, **kwargs):
            res = obj.split(',')
            return Foo(a = int(res[0]),
                       b = int(res[1]),
                       c = int(res[2]))

        jsons.set_serializer(foo_serializer, Foo,  True)
        jsons.set_deserializer(foo_deserializer, Foo,  True)

        bar: Dict[Foo, D] = {Foo(1, 2, 3): D(a=42, b=39)}
        dumped = jsons.dump(bar, cls=Dict[Foo, D],
                            strict=True,
                            strip_privates=True,
                            strip_properties=True,
                            use_enum_name = True)
        self.assertEqual(dumped, {'1,2,3': {"a": 42, "b": 39}})
        loaded = jsons.load(dumped, cls=Dict[Foo, D],
                            strict=True,
                            strip_privates=True,
                            strip_properties=True,
                            use_enum_name = True)
        self.assertEqual(loaded, bar)

    def test_dict_hashkey(self):
        bar: Dict[Foo, D] = {Foo(1, 2, 3): D(a=42, b=39)}
        dumped = jsons.dump(bar, cls=Dict[Foo, D],
                            strict=True,
                            strip_privates=True,
                            strip_properties=True,
                            use_enum_name = True)
        loaded = jsons.load(dumped, cls=Dict[Foo, D],
                            strict=True,
                            strip_privates=True,
                            strip_properties=True,
                            use_enum_name = True)
        self.assertEqual(loaded, bar)
