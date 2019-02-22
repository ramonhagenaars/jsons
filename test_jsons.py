import asyncio
import datetime
import json
from enum import Enum
from typing import List, Tuple, Set, Dict
from unittest.case import TestCase
import jsons
from jsons import JsonSerializable, KEY_TRANSFORMER_CAMELCASE
from jsons._common_impl import snakecase, camelcase, pascalcase, lispcase
from jsons.decorators import dumped, loaded
from jsons.deserializers import KEY_TRANSFORMER_SNAKECASE
from jsons.exceptions import UnfulfilledArgumentError, InvalidDecorationError, \
    DecodeError, SignatureMismatchError


class TestJsons(TestCase):

    def test_dump_str(self):
        self.assertEqual('some string', jsons.dump('some string'))

    def test_dump_int(self):
        self.assertEqual(123, jsons.dump(123))

    def test_dump_float(self):
        self.assertEqual(123.456, jsons.dump(123.456))

    def test_dump_bool(self):
        self.assertEqual(True, jsons.dump(True))

    def test_dump_dict(self):
        d = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                              tzinfo=datetime.timezone.utc)
        dict_ = {'a': {'b': {'c': {'d': d}}}}
        expectation = {'a': {'b': {'c': {'d': '2018-07-08T21:34:00Z'}}}}
        self.assertDictEqual(expectation, jsons.dump(dict_))

    def test_dump_none(self):
        self.assertEqual(None, jsons.dump(None))

    def test_dump_naive_datetime(self):
        d = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34)
        dumped = jsons.dump(d)
        self.assertTrue(dumped.startswith('2018-07-08T21:34:00'))
        self.assertTrue(not dumped.endswith('Z'))

    def test_dump_datetime_utcnow(self):
        d = datetime.datetime.utcnow()
        dumped = jsons.dump(d)
        # utcnow generates a datetime without tzinfo.
        self.assertTrue(not dumped.endswith('Z'))

    def test_dump_datetime_with_tzinfo(self):
        d = datetime.datetime.now(datetime.timezone.utc)
        dumped = jsons.dump(d)
        # utcnow generates a datetime without tzinfo.
        self.assertTrue(dumped.endswith('Z'))

    def test_dump_datetime_with_stripped_microseconds(self):
        d = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                              second=10, microsecond=123456,
                              tzinfo=datetime.timezone.utc)
        dumped = jsons.dump(d)
        self.assertEqual('2018-07-08T21:34:10Z', dumped)

    def test_dump_datetime_with_microseconds(self):
        d = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                              microsecond=123456, tzinfo=datetime.timezone.utc)
        dumped = jsons.dump(d, strip_microseconds=False)
        self.assertEqual('2018-07-08T21:34:00.123456Z', dumped)

    def test_dump_datetime_with_tz(self):
        tzinfo = datetime.timezone(datetime.timedelta(hours=-2))
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=tzinfo)
        dumped = jsons.dump(dat)
        self.assertEqual(dumped, '2018-07-08T21:34:00-02:00')

    def test_dump_enum(self):
        class E(Enum):
            x = 1
            y = 2
        self.assertEqual('x', jsons.dump(E.x))
        self.assertEqual(2, jsons.dump(E.y, use_enum_name=False))

    def test_dump_list(self):
        d = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                              tzinfo=datetime.timezone.utc)
        l = [1, 2, 3, [4, 5, [d]]]
        self.assertEqual([1, 2, 3, [4, 5, ['2018-07-08T21:34:00Z']]],
                         jsons.dump(l))

    def test_dump_tuple(self):
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        tup = (1, 2, 3, [4, 5, (dat,)])
        self.assertEqual([1, 2, 3, [4, 5, ['2018-07-08T21:34:00Z']]],
                         jsons.dump(tup))

    def test_dump_set(self):
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        set_ = {dat, dat}
        dumped = jsons.dump(set_)
        expected = ['2018-07-08T21:34:00Z']
        self.assertEqual(dumped, expected)

    class ParentDumpable:
        _par_c = 10

        def __init__(self):
            self.par_v = None

        @property
        def par_p(self):
            return 12

    class AllDumpable(ParentDumpable):
        c = 1
        _c = 2
        c_n = None
        _c_n = None

        def __init__(self, child=None):
            super().__init__()
            self.child = child
            self.v = 3
            self._v = 4
            self.v_n = None
            self._v_n = None

        @property
        def p(self):
            return 5

        @property
        def _p(self):
            return 5

        @property
        def p_n(self):
            return None

        @property
        def _p_n(self):
            return None

    def test_dump_object(self):
        obj = self.AllDumpable(self.AllDumpable())
        exp = {'_par_c': 10, 'par_v': None, 'par_p': 12,
               'c': 1, '_c': 2, 'c_n': None, '_c_n': None,
               'child': None, 'v': 3, '_v': 4, 'v_n': None, '_v_n': None,
               'p': 5, '_p': 5, 'p_n': None, '_p_n': None}
        exp['child'] = exp.copy()
        dump = jsons.dump(obj)
        self.assertDictEqual(exp, dump)

    def test_dump_object_strip_properties(self):
        obj = self.AllDumpable(self.AllDumpable())
        exp = {'_par_c': 10, 'par_v': None,
               'c': 1, '_c': 2, 'c_n': None, '_c_n': None,
               'child': None, 'v': 3, '_v': 4, 'v_n': None, '_v_n': None}
        exp['child'] = exp.copy()
        dump = jsons.dump(obj, strip_properties=True)
        self.assertDictEqual(exp, dump)

    def test_dump_object_strip_nulls(self):
        obj = self.AllDumpable(self.AllDumpable())
        exp = {'_par_c': 10, 'par_p': 12,
               'c': 1, '_c': 2, 'child': None, 'v': 3, '_v': 4, 'p': 5, '_p': 5}
        exp['child'] = exp.copy()
        exp['child'].pop('child')  # child shouldn't have None child
        dump = jsons.dump(obj, strip_nulls=True)
        self.assertDictEqual(exp, dump)

    def test_dump_object_strip_privates(self):
        obj = self.AllDumpable(self.AllDumpable())
        exp = {'par_v': None, 'par_p': 12,
               'c': 1, 'c_n': None,
               'child': None, 'v': 3, 'v_n': None, 'p': 5, 'p_n': None}
        exp['child'] = exp.copy()
        dump = jsons.dump(obj, strip_privates=True)
        self.assertDictEqual(exp, dump)

    def test_dump_object_strip_class_variables(self):
        obj = self.AllDumpable(self.AllDumpable())
        exp = {'par_v': None, 'par_p': 12,
               'child': None, 'v': 3, '_v': 4, 'v_n': None, '_v_n': None,
               'p': 5, '_p': 5, 'p_n': None, '_p_n': None}
        exp['child'] = exp.copy()
        dump = jsons.dump(obj, strip_class_variables=True)
        self.assertDictEqual(exp, dump)

    def test_dump_with_slots(self):
        class C:
            __slots__ = 'x', 'y'

            def __init__(self, x):
                self.x = x
                self.y = 'This is no parameter'

        c = C('something')
        dumped = jsons.dump(c)
        self.assertDictEqual(dumped, {'x': 'something',
                                      'y': 'This is no parameter'})

    def test_dump_as_parent_type(self):
        class Parent:
            __slots__ = ['parent_name']

            def __init__(self, pname):
                self.parent_name = pname

        class Child(Parent):
            def __init__(self, cname, pname):
                Parent.__init__(self, pname)
                self.child_name = cname

        c = Child('John', 'William')
        dumped1 = jsons.dump(c)
        dumped2 = jsons.dump(c, Parent)
        self.assertDictEqual(dumped1, {'child_name': 'John',
                                       'parent_name': 'William'})
        self.assertDictEqual(dumped2, {'parent_name': 'William'})

    def test_dumped_decorator(self):
        class Base:
            __slots__ = ['y']

            def __init__(self, x):
                self.y = x

        class C(Base):
            def __init__(self, x):
                Base.__init__(self, x)
                self.x = x

        @dumped()
        def func1(c1):
            self.assertEqual(c1['x'], 'c1')
            return C('c_res')

        @dumped(returnvalue=False)
        def func2(c1):
            self.assertEqual(c1['x'], 'c1')
            return C('c_res')

        @dumped(parameters=False)
        def func3(c1):
            self.assertEqual(c1.x, 'c1')
            return C('c_res')

        @dumped()
        def func4(c1: Base) -> Base:
            self.assertEqual(c1['y'], 'c1')
            self.assertFalse(hasattr(c1, 'x'))
            return C('c_res')

        @dumped(key_transformer=jsons.KEY_TRANSFORMER_PASCALCASE)
        def func5(c1):
            self.assertTrue('X' in c1)
            self.assertFalse('x' in c1)
            return C('c_res')

        c1 = C('c1')

        self.assertEqual(func1(c1)['x'], 'c_res')
        self.assertEqual(func2(c1).x, 'c_res')
        self.assertEqual(func3(c1)['x'], 'c_res')
        self.assertEqual(func4(c1)['y'], 'c_res')
        self.assertFalse(hasattr(func4(c1), 'x'), 'c_res')
        self.assertEqual(func5(c1)['X'], 'c_res')

    def test_dumped_decorator_async(self):
        class C:
            def __init__(self, x):
                self.x = x

        @dumped()
        async def func1(c1):
            self.assertEqual(c1['x'], 'c1')
            return C('c_res')

        async def _test_body():
            c1 = C('c1')
            res = await func1(c1)
            self.assertEqual(res['x'], 'c_res')

        asyncio.get_event_loop().run_until_complete(_test_body())

    def test_dumped_decorator_on_method(self):
        class C1:
            def __init__(self, x):
                self.x = x

        class C2:
            @dumped()
            def method1(self, c1):
                self_.assertTrue(isinstance(self, C2))
                self_.assertEqual(c1['x'], 'c1')
                return C1('res1')

            @classmethod
            @dumped()
            def method2(cls, c1):
                self_.assertEqual(cls, C2)
                self_.assertEqual(c1['x'], 'c1')
                return C1('res2')

            @staticmethod
            @dumped()
            def method3(c1):
                self_.assertEqual(c1['x'], 'c1')
                return C1('res3')

        self_ = self

        res1 = C2().method1(C1('c1'))
        res2 = C2().method2(C1('c1'))
        res3 = C2().method3(C1('c1'))
        self.assertEqual(res1['x'], 'res1')
        self.assertEqual(res2['x'], 'res2')
        self.assertEqual(res3['x'], 'res3')

        with self.assertRaises(InvalidDecorationError):
            class Clazz:
                @dumped()
                @staticmethod
                def method4(c1):
                    pass  # This won't work; you need to swap the decorators.

    def test_dumped_decorator_on_class(self):
        with self.assertRaises(InvalidDecorationError):
            @loaded()
            class Clazz:
                pass

    def test_load_str(self):
        self.assertEqual('some string', jsons.load('some string'))

    def test_load_int(self):
        self.assertEqual(123, jsons.load(123))

    def test_load_float(self):
        self.assertEqual(123.456, jsons.load(123.456))

    def test_load_bool(self):
        self.assertEqual(True, jsons.load(True))

    def test_load_dict(self):
        dumped = {'a': {'b': {'c': {'d': '2018-07-08T21:34:00Z'}}}}
        loaded = jsons.load(dumped)
        self.assertEqual(loaded['a']['b']['c']['d'].year, 2018)
        self.assertEqual(loaded['a']['b']['c']['d'].month, 7)
        self.assertEqual(loaded['a']['b']['c']['d'].day, 8)
        self.assertEqual(loaded['a']['b']['c']['d'].hour, 21)
        self.assertEqual(loaded['a']['b']['c']['d'].minute, 34)
        self.assertEqual(loaded['a']['b']['c']['d'].second, 0)

    def test_load_dict_with_generic(self):
        class A:
            def __init__(self):
                self.name = 'A'

        class B:
            def __init__(self, a: A):
                self.a = a
                self.name = 'B'

        dumped_b = {'a': {'name': 'A'}, 'name': 'B'}
        dumped_dict = {'b_inst': dumped_b}
        loaded = jsons.load(dumped_dict, Dict[str, B])

        self.assertEqual(loaded['b_inst'].a.name, 'A')

    def test_load_partially_deserialized_dict(self):
        class C:
            def __init__(self, d: datetime.datetime):
                self.d = d

        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        dumped = {'d': dat}
        loaded = jsons.load(dumped, C)

        self.assertEqual(loaded.d, dat)

    def test_load_partially_deserialized_dict_in_strict_mode(self):
        class C:
            def __init__(self, d: datetime.datetime):
                self.d = d

        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        dumped = {'d': dat}
        with self.assertRaises(ValueError):
            jsons.load(dumped, C, strict=True)

    def test_load_none(self):
        self.assertEqual(None, jsons.load(None))
        self.assertEqual(None, jsons.load(None, datetime))
        with self.assertRaises(ValueError):
            jsons.load(None, datetime, strict=True)

    def test_load_too_many_args(self):
        class C:
            def __init__(self, x: int):
                self.x = x

        with self.assertRaises(SignatureMismatchError):
            jsons.load({'x': 1, 'y': 2}, C, strict=True)

        try:
            jsons.load({'x': 1, 'y': 2}, C, strict=True)
        except SignatureMismatchError as err:
            self.assertEqual(err.argument, 'y')
            self.assertEqual(err.target, C)
            self.assertDictEqual(err.source, {'x': 1, 'y': 2})


    def test_load_datetime(self):
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        self.assertEqual(dat, jsons.load('2018-07-08T21:34:00Z'))

    def test_load_datetime_with_tz(self):
        tzinfo = datetime.timezone(datetime.timedelta(hours=-2))
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=tzinfo)
        loaded = jsons.load('2018-07-08T21:34:00-02:00')
        self.assertEqual(loaded, dat)

    def test_load_enum(self):
        class E(Enum):
            x = 1
            y = 2

        self.assertEqual(E.x, jsons.load('x', E))
        self.assertEqual(E.y, jsons.load(2, E, use_enum_name=False))

    def test_load_list(self):
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        list_ = [1, 2, 3, [4, 5, [dat]]]
        expectation = [1, 2, 3, [4, 5, ['2018-07-08T21:34:00Z']]]
        self.assertEqual(list_, jsons.load(expectation))

    def test_load_tuple(self):
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        tup = (1, ([dat],))
        expectation = (1, (['2018-07-08T21:34:00Z'],))
        cls = Tuple[int, Tuple[List[datetime.datetime]]]
        self.assertEqual(tup, jsons.load(expectation, cls))

    def test_load_tuple_with_n_length(self):
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        expectation = (dat, dat)
        loaded = jsons.load(['2018-07-08T21:34:00Z',
                             '2018-07-08T21:34:00Z'],
                            cls=Tuple[datetime.datetime, ...])
        self.assertEqual(expectation, loaded)

    def test_load_set(self):
        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        loaded1 = jsons.load(['2018-07-08T21:34:00Z'], set)
        loaded2 = jsons.load(['2018-07-08T21:34:00Z'], Set[str])
        self.assertEqual(loaded1, {dat})
        self.assertEqual(loaded2, {'2018-07-08T21:34:00Z'})

    def test_load_object(self):
        class A:
            def __init__(self):
                self.name = 'A'

        class B:
            def __init__(self, a: A):
                self.a = a
                self.name = 'B'

        b = B(A())
        loaded_b = jsons.load({'name': 'B', 'a': {'name': 'A'}}, B)
        self.assertEqual(b.name, loaded_b.name)
        self.assertEqual(b.a.name, loaded_b.a.name)

    def test_load_object_with_attr_getters(self):
        class A:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        class B:
            def __init__(self, x):
                self.x = x

        a = A(1, 2)
        loaded_a = jsons.load({'x': 1}, A, attr_getters={'y': lambda: 2})
        self.assertEqual(a.x, loaded_a.x)
        self.assertEqual(a.y, loaded_a.y)

        b = B(1)
        loaded_b = jsons.load({'x': 1}, B, attr_getters={'y': lambda: 2})
        self.assertEqual(b.x, loaded_b.x)
        self.assertEqual(2, loaded_b.y)

    def test_load_object_with_default_value(self):
        class A:
            def __init__(self, x, y = 2):
                self.x = x
                self.y = y

        a = A(1)
        loaded_a = jsons.load({'x': 1}, A)
        self.assertEqual(a.x, loaded_a.x)
        self.assertEqual(a.y, loaded_a.y)

    def test_dump_load_object_deep(self):
        class A:
            def __init__(self):
                self.name = 'A'

        class B:
            def __init__(self, list_a: List[A],
                         list_dates: List[datetime.datetime]):
                self.list_a = list_a
                self.list_dates = list_dates
                self.name = 'B'

        class C:
            def __init__(self, list_b: List[B]):
                self.list_b = list_b

        c = C([B([A(), A()], []),
               B([], [datetime.datetime.now(), datetime.datetime.now()])])
        dumped_c = jsons.dump(c)
        loaded_c = jsons.load(dumped_c, C)
        self.assertEqual(loaded_c.list_b[0].name, 'B')
        self.assertEqual(loaded_c.list_b[0].list_a[0].name, 'A')
        self.assertEqual(loaded_c.list_b[0].list_a[1].name, 'A')
        self.assertEqual(loaded_c.list_b[1].list_dates[0].year,
                         c.list_b[1].list_dates[0].year)
        self.assertEqual(loaded_c.list_b[1].list_dates[0].month,
                         c.list_b[1].list_dates[0].month)
        self.assertEqual(loaded_c.list_b[1].list_dates[0].day,
                         c.list_b[1].list_dates[0].day)
        self.assertEqual(loaded_c.list_b[1].list_dates[0].hour,
                         c.list_b[1].list_dates[0].hour)
        self.assertEqual(loaded_c.list_b[1].list_dates[0].minute,
                         c.list_b[1].list_dates[0].minute)
        self.assertEqual(loaded_c.list_b[1].list_dates[0].second,
                         c.list_b[1].list_dates[0].second)

    def test_load_object_properties(self):
        class WithoutSetter:
            @property
            def x(self):
                return 123

        class WithSetter:
            def __init__(self):
                self.__x = 123
            @property
            def x(self):
                return self.__x

            @x.setter
            def x(self, x):
                self.__x = x

        loaded1 = jsons.load({'x': 123}, WithoutSetter)
        self.assertEqual(loaded1.x, 123)

        loaded2 = jsons.load({'x': 456}, WithSetter)
        self.assertEqual(loaded2.x, 456)

    def test_load_slots(self):
        class ClassWithSlots:
            __slots__ = 'x', 'y'

            def __init__(self, x):
                self.x = x
                self.y = 'This is not a parameter'

        class ClassWithoutSlots:
            def __init__(self, x):
                self.x = x
                self.y = 'This is not a parameter'

        raw = {'x': 'something', 'y': 'something else', 'z': 'uh oh...'}
        loaded_with_slots = jsons.load(raw, cls=ClassWithSlots)
        loaded_without_slots = jsons.load(raw, cls=ClassWithoutSlots)

        self.assertTrue(hasattr(loaded_with_slots, 'x'))
        self.assertTrue(hasattr(loaded_with_slots, 'y'))
        self.assertTrue(not hasattr(loaded_with_slots, 'z'))

        self.assertTrue(hasattr(loaded_without_slots, 'x'))
        self.assertTrue(hasattr(loaded_without_slots, 'y'))
        self.assertTrue(hasattr(loaded_without_slots, 'z'))

    def test_dumps(self):
        class A:
            def __init__(self):
                self.name = 'A'

        class B:
            def __init__(self, a: A):
                self.a = a
                self.name = 'B'

        sdumped = jsons.dumps(B(A()))
        s = json.dumps({'a': {'name': 'A'}, 'name': 'B'})
        self.assertDictEqual(eval(s), eval(sdumped))

    def test_loads(self):
        class A:
            def __init__(self):
                self.name = 'A'

        class B:
            def __init__(self, a: A):
                self.a = a
                self.name = 'B'

        s = json.dumps({'a': {'name': 'A'}, 'name': 'B'})
        loaded_dict = jsons.loads(s)
        self.assertEqual('B', loaded_dict['name'])
        self.assertEqual('A', loaded_dict['a']['name'])

        loaded_obj = jsons.loads(s, B)
        self.assertEqual('B', loaded_obj.name)
        self.assertEqual('A', loaded_obj.a.name)

    def test_dumpb(self):
        class A:
            def __init__(self):
                self.name = 'A'

        class B:
            def __init__(self, a: A):
                self.a = a
                self.name = 'B'

        dumped = jsons.dumpb(B(A()), jdkwargs={'sort_keys': True})
        b = json.dumps({'a': {'name': 'A'}, 'name': 'B'},
                       sort_keys=True).encode()
        self.assertEqual(b, dumped)

    def test_loadb(self):
        class A:
            def __init__(self):
                self.name = 'A'

        class B:
            def __init__(self, a: A):
                self.a = a
                self.name = 'B'

        b = json.dumps({'a': {'name': 'A'}, 'name': 'B'}).encode()
        loaded_dict = jsons.loadb(b)

        self.assertDictEqual(loaded_dict, {'a': {'name': 'A'}, 'name': 'B'})

        loaded_obj = jsons.loadb(b, B)
        self.assertEqual('B', loaded_obj.name)
        self.assertEqual('A', loaded_obj.a.name)

    def test_jsonserializable(self):
        class Person(JsonSerializable):
            def __init__(self, name, age):
                self.name = name
                self.age = age

        person = Person('John', 65)
        person_json = person.json
        person_json_str = person.dumps()
        person_json_bytes = person.dumpb()
        person_loaded = Person.from_json(person_json)
        person_loaded_str = str(person_json)
        person_loaded_bytes = Person.loadb(b'{"name": "John", "age": 65}')

        self.assertDictEqual(person_json, {'name': 'John', 'age': 65})
        self.assertDictEqual(person.dump(), {'name': 'John', 'age': 65})
        self.assertDictEqual(eval(person_json_str),
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

    def test_jsonserializable_with_kwargs(self):
        forked = JsonSerializable\
            .with_dump(fork=True, key_transformer=KEY_TRANSFORMER_CAMELCASE)
        forked.with_load(key_transformer=KEY_TRANSFORMER_SNAKECASE)

        class Person(forked):
            def __init__(self, my_name):
                self.my_name = my_name

        person = Person('John')
        person_json = person.json  # should have camelCase
        person_loaded = Person.from_json(person_json)  # should have snake_case

        self.assertDictEqual(person_json, {'myName': 'John'})
        self.assertEqual(person_loaded.my_name, 'John')
        self.assertTrue(isinstance(person_loaded, Person))

    def test_jsonserializable_fork(self):
        f1 = JsonSerializable.fork()
        f2 = JsonSerializable.fork()

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
        f1 = JsonSerializable.fork()
        f1.set_serializer(lambda *_, **__: 'f1', str)

        f2 = f1.fork()
        f2.set_serializer(lambda *_, **__: 'f2', str)
        f2.set_serializer(lambda *_, **__: 999, int)

        f3 = f2.fork('custom_fork_name')
        f3.set_serializer(lambda *_, **__: 'f3', str)

        self.assertEqual(jsons.dump('some string', fork_inst=f1), 'f1')
        self.assertEqual(jsons.dump(123, fork_inst=f1), 123)

        self.assertEqual(jsons.dump('some string', fork_inst=f2), 'f2')
        self.assertEqual(jsons.dump(123, fork_inst=f2), 999)

        self.assertEqual(jsons.dump('some string', fork_inst=f3), 'f3')
        self.assertEqual(jsons.dump(123, fork_inst=f3), 999)
        self.assertEqual(f3.__name__, 'custom_fork_name')

    def test_case_transformers(self):
        camelcase_str = 'camelCase'
        snakecase_str = 'snake_case'
        pascalcase_str = 'Pascal_case'
        pascalcase_str2 = 'ABcDe'
        lispcase_str = 'lisp-case'

        self.assertEqual(camelcase(camelcase_str), 'camelCase')
        self.assertEqual(camelcase(snakecase_str), 'snakeCase')
        self.assertEqual(camelcase(pascalcase_str), 'pascalCase')
        self.assertEqual(camelcase(pascalcase_str2), 'aBcDe')
        self.assertEqual(camelcase(lispcase_str), 'lispCase')

        self.assertEqual(snakecase(camelcase_str), 'camel_case')
        self.assertEqual(snakecase(snakecase_str), 'snake_case')
        self.assertEqual(snakecase(pascalcase_str), 'pascal_case')
        self.assertEqual(snakecase(pascalcase_str2), 'a_bc_de')
        self.assertEqual(snakecase(lispcase_str), 'lisp_case')

        self.assertEqual(pascalcase(camelcase_str), 'CamelCase')
        self.assertEqual(pascalcase(snakecase_str), 'SnakeCase')
        self.assertEqual(pascalcase(pascalcase_str), 'PascalCase')
        self.assertEqual(pascalcase(pascalcase_str2), 'ABcDe')
        self.assertEqual(pascalcase(lispcase_str), 'LispCase')

        self.assertEqual(lispcase(camelcase_str), 'camel-case')
        self.assertEqual(lispcase(snakecase_str), 'snake-case')
        self.assertEqual(lispcase(pascalcase_str), 'pascal-case')
        self.assertEqual(lispcase(pascalcase_str2), 'a-bc-de')
        self.assertEqual(lispcase(lispcase_str), 'lisp-case')

    def test_serialize_and_deserialize_with_case_transformer(self):
        class A:
            def __init__(self, snake_case_str, some_dict):
                self.snake_case_str = snake_case_str
                self.some_dict = some_dict

        class B:
            def __init__(self, a_obj: A, camel_case_str):
                self.a_obj = a_obj
                self.camel_case_str = camel_case_str

        b = B(A('one_two', {'some_key': 'some_value'}), 'theeFour')
        dumped_pascalcase = \
            jsons.dump(b, key_transformer=jsons.KEY_TRANSFORMER_PASCALCASE)
        loaded_snakecase = \
            jsons.load(dumped_pascalcase, B,
                       key_transformer=jsons.KEY_TRANSFORMER_SNAKECASE)
        expected_dump = {
            'AObj': {
                'SnakeCaseStr': 'one_two',
                'SomeDict': {
                    'SomeKey': 'some_value'
                }
            },
            'CamelCaseStr': 'theeFour'
        }
        self.assertEqual(expected_dump, dumped_pascalcase)
        self.assertEqual(loaded_snakecase.camel_case_str, 'theeFour')
        self.assertEqual(loaded_snakecase.a_obj.snake_case_str, 'one_two')
        self.assertEqual(loaded_snakecase.a_obj.some_dict['some_key'],
                         'some_value')

    def test_set_custom_functions(self):
        jsons.set_serializer(lambda *_, **__: 'custom_serializer', str)
        jsons.set_deserializer(lambda *_, **__: 'custom_deserializer', str)

        dumped = jsons.dump('serialize me')
        loaded = jsons.load(dumped)

        self.assertEqual(dumped, 'custom_serializer')
        self.assertEqual(loaded, 'custom_deserializer')

    def test_loaded_decorator(self):
        class C:
            def __init__(self, x):
                self.x = x

        @loaded()
        def func1(c1, c2: C) -> C:
            self.assertEqual(c1['x'], 'c1')
            self.assertEqual(c2.x, 'c2')
            return jsons.dump(C('c_res'))

        @loaded()
        def func2(c1, c2: C):
            self.assertEqual(c1['x'], 'c1')
            self.assertEqual(c2.x, 'c2')
            return jsons.dump(C('c_res'))

        @loaded(returnvalue=False)
        def func3(c1, c2: C) -> C:
            self.assertEqual(c1['x'], 'c1')
            self.assertEqual(c2.x, 'c2')
            return jsons.dump(C('c_res'))

        @loaded(parameters=False)
        def func4(c1, c2: C) -> C:
            self.assertEqual(c1['x'], 'c1')
            self.assertEqual(c2['x'], 'c2')
            return jsons.dump(C('c_res'))

        @loaded(key_transformer=jsons.KEY_TRANSFORMER_SNAKECASE)
        def func5(c1, c2: C) -> C:
            self.assertEqual(c1['x'], 'c3')
            self.assertEqual(c2.x, 'c3')
            return {'X': 'c_res'}

        c1 = jsons.dump(C('c1'))
        c2 = jsons.dump(C('c2'))
        c3 = {'X': 'c3'}

        self.assertEqual(func1(c1, c2).x, 'c_res')
        self.assertEqual(func2(c1, c2)['x'], 'c_res')
        self.assertEqual(func3(c1, c2)['x'], 'c_res')
        self.assertEqual(func4(c1, c2).x, 'c_res')
        self.assertEqual(func5(c3, c3).x, 'c_res')

    def test_loaded_with_loader(self):
        class C:
            def __init__(self, x):
                self.x = x

        @loaded(loader=jsons.loads)
        def func_s(c: C) -> C:
            self.assertEqual(c.x, 'c1')
            return '{"x": "res1"}'

        @loaded(loader=jsons.loadb)
        def func_b(c: C) -> C:
            self.assertEqual(c.x, 'c2')
            return b'{"x": "res2"}'

        s = '{"x": "c1"}'
        b = b'{"x": "c2"}'
        self.assertEqual(func_s(s).x, 'res1')
        self.assertEqual(func_b(b).x, 'res2')

    def test_loaded_and_dumped_decorator(self):
        @dumped(parameters=False)
        @loaded(returnvalue=False)
        def func(x):
            return x
        arg = '2018-10-07T19:45:00+02:00'
        res = func(arg)
        self.assertEqual(arg, res)

    def test_loaded_decorator_async(self):
        class C:
            def __init__(self, x):
                self.x = x

        @loaded()
        async def func1(c1, c2: C) -> C:
            self.assertEqual(c1['x'], 'c1')
            self.assertEqual(c2.x, 'c2')
            return jsons.dump(C('c_res'))

        async def _test_body():
            c1 = jsons.dump(C('c1'))
            c2 = jsons.dump(C('c2'))
            res = await func1(c1, c2)
            self.assertEqual(res.x, 'c_res')

        asyncio.get_event_loop().run_until_complete(_test_body())

    def test_exception_unfulfilled_arg(self):
        class C:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        with self.assertRaises(UnfulfilledArgumentError):
            jsons.load({"x": 1}, C)

        try:
            jsons.load({"x": 1}, C)
        except UnfulfilledArgumentError as err:
            self.assertDictEqual({"x": 1}, err.source)
            self.assertEqual(C, err.target)
            self.assertEqual('y', err.argument)

    def test_exception_wrong_json(self):
        with self.assertRaises(DecodeError):
            jsons.loads('{this aint no JSON!')

        try:
            jsons.loads('{this aint no JSON!')
        except DecodeError as err:
            self.assertEqual(None, err.target)
            self.assertEqual('{this aint no JSON!', err.source)

    def test_exception_wrong_bytes(self):
        with self.assertRaises(ValueError):
            jsons.loadb('{"key": "value"}')
