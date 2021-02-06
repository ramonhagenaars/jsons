import datetime
from unittest import TestCase

import jsons


class TestJsonSerializable(TestCase):
    def test_jsonserializable(self):
        class Person(jsons.JsonSerializable):
            def __init__(self, name, age):
                self.name = name
                self.age = age

        person = Person('John', 65)
        person_json = person.json
        person_json_str = person.dumps()
        person_json_str2 = str(person)
        person_json_bytes = person.dumpb()
        person_loaded = Person.from_json(person_json)
        person_loaded_str = str(person_json)
        person_loaded_bytes = Person.loadb(b'{"name": "John", "age": 65}')

        self.assertDictEqual(person_json, {'name': 'John', 'age': 65})
        self.assertDictEqual(person.dump(), {'name': 'John', 'age': 65})
        self.assertDictEqual(eval(person_json_str),
                             eval("{'name': 'John', 'age': 65}"))
        self.assertDictEqual(eval(person_json_str2),
                             eval("{'name': 'John', 'age': 65}"))
        self.assertDictEqual(eval(person_json_bytes.decode()),
                             eval("{'name': 'John', 'age': 65}"))
        self.assertDictEqual(eval(person_loaded_str),
                             eval("{'name': 'John', 'age': 65}"))
        self.assertEqual(person_loaded.name, 'John')
        self.assertEqual(person_loaded.age, 65)
        self.assertEqual(person_loaded_bytes.name, 'John')
        self.assertEqual(Person.load(person_json).name, 'John')
        self.assertEqual(Person.load(person_json).age, 65)
        self.assertEqual(Person.loads(person_json_str).age, 65)

    def test_jsonserializable_with_kwargs(self):
        forked = jsons.JsonSerializable \
            .with_dump(fork=True, key_transformer=jsons.KEY_TRANSFORMER_CAMELCASE)
        forked.with_load(key_transformer=jsons.KEY_TRANSFORMER_SNAKECASE)

        class Person(forked):
            def __init__(self, my_name):
                self.my_name = my_name

        person = Person('John')
        person_json = person.json  # should have camelCase
        person_loaded = Person.from_json(person_json)  # should have snake_case

        self.assertDictEqual(person_json, {'myName': 'John'})
        self.assertEqual(person_loaded.my_name, 'John')
        self.assertTrue(isinstance(person_loaded, Person))

    def test_with_load(self):
        defaults = {'ham': lambda: 'spam'}
        forked = jsons.JsonSerializable.with_load(attr_getters=defaults, fork=True)
        forked.set_deserializer(
            lambda sec, cls, **kwargs: datetime.timedelta(seconds=sec),
            datetime.timedelta
        )

        class Foo(forked):
            def __init__(self, bar: datetime.timedelta, ham: str):
                self.bar = bar
                self.ham = ham

        loaded = Foo.from_json({'bar': 42})
        self.assertEqual('spam', loaded.ham)
        self.assertEqual(datetime.timedelta(seconds=42), loaded.bar)

    def test_jsonserializable_fork(self):
        f1 = jsons.JsonSerializable.fork()
        f2 = jsons.JsonSerializable.fork()

        self.assertNotEqual(f1, f2)
        self.assertNotEqual(f1.__name__, f2.__name__)

        f1.set_serializer(lambda *_, **__: 'f1', str)
        f2.set_serializer(lambda *_, **__: 'f2', str)

        class C1(f1):
            def __init__(self):
                self.x = 'some string'

        class C2(f2):
            def __init__(self):
                self.x = 'some string'

        c1 = C1()
        c2 = C2()

        self.assertDictEqual(c1.json, {'x': 'f1'})
        self.assertDictEqual(c2.json, {'x': 'f2'})
        self.assertEqual(jsons.dump(c1.x), 'some string')
        self.assertEqual(jsons.dump(c1.x, fork_inst=f1), 'f1')
        self.assertEqual(jsons.dump(c1.x, fork_inst=f2), 'f2')  # Note: c1.x!

    def test_jsonserializable_fork_of_forks(self):
        f1 = jsons.JsonSerializable.fork()
        f1.set_serializer(lambda *_, **__: 'f1', str)

        f2 = f1.fork()
        f2.set_serializer(lambda *_, **__: 'f2', str)
        f2.set_serializer(lambda *_, **__: 999, int)
        f2.set_deserializer(lambda *_, **__: 42, int)

        f3 = f2.fork('custom_fork_name')
        f3.set_serializer(lambda *_, **__: 'f3', str)
        f3.set_deserializer(lambda *_, **__: 84, int)

        self.assertEqual(jsons.dump('some string', fork_inst=f1), 'f1')
        self.assertEqual(jsons.dump(123, fork_inst=f1), 123)
        self.assertEqual(jsons.load(123, fork_inst=f1), 123)

        self.assertEqual(jsons.dump('some string', fork_inst=f2), 'f2')
        self.assertEqual(jsons.dump(123, fork_inst=f2), 999)
        self.assertEqual(jsons.load(123, fork_inst=f2), 42)

        self.assertEqual(jsons.dump('some string', fork_inst=f3), 'f3')
        self.assertEqual(jsons.dump(123, fork_inst=f3), 999)
        self.assertEqual(jsons.load(123, fork_inst=f3), 84)
        self.assertEqual(f3.__name__, 'custom_fork_name')
