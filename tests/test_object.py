import datetime
import warnings
from abc import ABC
from typing import List, Dict
from unittest import TestCase
from jsons._common_impl import StateHolder
from jsons.exceptions import SignatureMismatchError, UnknownClassError, \
    SerializationError
import jsons


class TestObject(TestCase):
    def test_dump_object(self):
        obj = AllDumpable(AllDumpable())
        exp = {'_par_c': 10, 'par_v': None, 'par_p': 12,
               'c': 1, '_c': 2, 'c_n': None, '_c_n': None,
               'child': None, 'v': 3, '_v': 4, 'v_n': None, '_v_n': None,
               'p': 5, '_p': 5, 'p_n': None, '_p_n': None}
        exp['child'] = exp.copy()
        dump = jsons.dump(obj)
        self.assertDictEqual(exp, dump)

    def test_dump_object_verbose(self):
        class A:
            def __init__(self, x):
                self.x = x

        class B:
            def __init__(self, a: A):
                self.a = a

        class C:
            def __init__(self, b: B):
                self.b = b

        c = C(B(A(42)))
        dumped = jsons.dump(c, verbose=jsons.Verbosity.WITH_CLASS_INFO)
        expectation = {
            'classes': {
                '/': '{}.C'.format(__name__),
                '/b': '{}.B'.format(__name__),
                '/b/a': '{}.A'.format(__name__)
            }
        }

        self.assertDictEqual(expectation, dumped['-meta'])

        dumped2 = jsons.dump(c, verbose=jsons.Verbosity.WITH_NOTHING)
        self.assertDictEqual({'b': {'a': {'x': 42}}}, dumped2)

        dumped3 = jsons.dump(c, verbose=jsons.Verbosity.WITH_DUMP_TIME)
        self.assertTrue('dump_time' in dumped3['-meta'])
        self.assertTrue('classes' not in dumped3['-meta'])

        dumped4 = jsons.dump(c, verbose=jsons.Verbosity.WITH_EVERYTHING)
        self.assertTrue('dump_time' in dumped4['-meta'])
        self.assertTrue('classes' in dumped4['-meta'])

    def test_dump_object_verbose_with_dict(self):

        class C:
            def __init__(self, d: Dict[int, float]):
                self.d = d

        c = C({42: 42.0})

        expectation = {
            'classes': {
                '/': '{}.C'.format(__name__),
                '/d': 'typing.Dict[int, float]',
            }
        }

        dumped = jsons.dump(c, verbose=jsons.Verbosity.WITH_CLASS_INFO)
        self.assertDictEqual(expectation, dumped['-meta'])

        loaded = jsons.load(dumped)

        self.assertDictEqual({42: 42.0}, loaded.d)

    def test_dump_object_strip_properties(self):
        obj = AllDumpable(AllDumpable())
        exp = {'_par_c': 10, 'par_v': None,
               'c': 1, '_c': 2, 'c_n': None, '_c_n': None,
               'child': None, 'v': 3, '_v': 4, 'v_n': None, '_v_n': None}
        exp['child'] = exp.copy()
        dump = jsons.dump(obj, strip_properties=True)
        self.assertDictEqual(exp, dump)

    def test_dump_object_strip_nulls(self):
        obj = AllDumpable(AllDumpable())
        exp = {'_par_c': 10, 'par_p': 12,
               'c': 1, '_c': 2, 'child': None, 'v': 3, '_v': 4, 'p': 5, '_p': 5}
        exp['child'] = exp.copy()
        exp['child'].pop('child')  # child shouldn't have None child
        dump = jsons.dump(obj, strip_nulls=True)
        self.assertDictEqual(exp, dump)

    def test_dump_object_strip_privates(self):
        obj = AllDumpable(AllDumpable())
        exp = {'par_v': None, 'par_p': 12,
               'c': 1, 'c_n': None,
               'child': None, 'v': 3, 'v_n': None, 'p': 5, 'p_n': None}
        exp['child'] = exp.copy()
        dump = jsons.dump(obj, strip_privates=True)
        self.assertDictEqual(exp, dump)

    def test_dump_object_strip_class_variables(self):
        obj = AllDumpable(AllDumpable())
        exp = {'par_v': None, 'par_p': 12,
               'child': None, 'v': 3, '_v': 4, 'v_n': None, '_v_n': None,
               'p': 5, '_p': 5, 'p_n': None, '_p_n': None}
        exp['child'] = exp.copy()
        dump = jsons.dump(obj, strip_class_variables=True)
        self.assertDictEqual(exp, dump)

    def test_dump_object_strip_attr(self):
        obj = AllDumpable(AllDumpable())
        dump1 = jsons.dump(obj, strip_attr='v')
        dump2 = jsons.dump(obj, strip_attr=('v', '_v'))
        exp1 = {'_par_c': 10, 'par_v': None, 'par_p': 12,
                'c': 1, '_c': 2, 'c_n': None, '_c_n': None,
                'child': None, '_v': 4, 'v_n': None, '_v_n': None, 'p': 5,
                '_p': 5, 'p_n': None, '_p_n': None}
        exp1['child'] = exp1.copy()
        exp2 = {'_par_c': 10, 'par_v': None, 'par_p': 12,
                'c': 1, '_c': 2, 'c_n': None, '_c_n': None,
                'child': None, 'v_n': None, '_v_n': None,
                'p': 5, '_p': 5, 'p_n': None, '_p_n': None}
        exp2['child'] = exp2.copy()
        self.assertDictEqual(exp1, dump1)
        self.assertDictEqual(exp2, dump2)

    def test_dump_abc_class(self):
        class A(ABC):
            pass

        class B(A):
            def __init__(self, x: int):
                self.x = x

        dumped = jsons.dump(B(42))
        self.assertDictEqual({'x': 42}, dumped)

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
        dumped2 = jsons.dump(c, cls=Parent, strict=True)
        self.assertDictEqual({'child_name': 'John',
                              'parent_name': 'William'}, dumped1)
        self.assertDictEqual({'parent_name': 'William'}, dumped2)

    def test_dump_with_error(self):
        class C:
            @property
            def x(self):
                raise KeyError('Some bug this is!')

        with self.assertRaises(SerializationError):
            jsons.dump(C())

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

    def test_load_object_verbose(self):
        class BarBase:
            pass

        class BarA(BarBase):
            def __init__(self, a: int):
                self.a = a

        class BarB(BarBase):
            def __init__(self, b: int):
                self.b = b

        class Foo(BarBase):
            def __init__(self, bar: BarBase):
                self.bar = bar

        jsons.announce_class(Foo)
        jsons.announce_class(BarA)
        jsons.announce_class(BarB)
        jsons.announce_class(BarBase)

        foo = Foo(bar=BarA(a=5))
        dumped = jsons.dump(foo, verbose=True)
        loaded = jsons.load(dumped)

        self.assertTrue(isinstance(loaded, Foo))
        self.assertTrue(isinstance(loaded.bar, BarA))

    def test_load_object_without_type_hints_verbose(self):
        class A:
            def __init__(self, x):
                self.x = x

        class B:
            def __init__(self, a: A):
                self.a = a

        class C:
            def __init__(self, b: B):
                self.b = b

        dumped1 = {
            'b': {
                'a': {
                    'x': 42
                }
            },
            '-meta': {
                'classes': {
                    '/': 'jsons.C',
                    '/b': 'jsons.B',
                    '/b/a': 'jsons.A'
                }
            }
        }

        # Place the classes where they can be found.
        jsons.A = A
        jsons.B = B
        jsons.C = C
        loaded = jsons.load(dumped1)
        # Clean it up again...
        del jsons.A
        del jsons.B
        del jsons.C
        self.assertEqual(42, loaded.b.a.x)

        # Now let's test what happens when we try to load an unknown class.
        dumped2 = {
            'x': 100,
            '-meta': {
                'classes': {
                    '/': 'custom_class'
                }
            }
        }

        with self.assertRaises(UnknownClassError):
            jsons.load(dumped2)

        try:
            jsons.load(dumped2)
        except UnknownClassError as err:
            self.assertEqual('custom_class', err.target_name)

        # Now announce the class and try again; it should work now.
        jsons.announce_class(A, 'custom_class')
        loaded2 = jsons.load(dumped2)
        self.assertEqual(100, loaded2.x)

    def test_dump_load_object_verbose_without_announcing(self):
        class A:
            def __init__(self, x):
                self.x = x

        class B:
            def __init__(self, a: A):
                self.a = a

        class C:
            def __init__(self, b: B):
                self.b = b

        c = C(B(A(42)))

        dumped = jsons.dump(c, verbose=True)
        loaded = jsons.load(dumped)

        self.assertEqual(42, loaded.b.a.x)

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

    def test_dump_load_object_verbose(self):
        h = StateHolder()
        dumped = jsons.dump(h, verbose=True)
        loaded = jsons.load(dumped)
        self.assertEqual(type(h), type(loaded))

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

    def test_dump_with_attr_fail(self):
        class FailingClass:
            @property
            def i_will_fail(self):
                raise KeyError('Told you so')

        class C:
            def __init__(self, x: int, y: FailingClass):
                self.x = x
                self.y = y

        c = C(42, FailingClass())

        with warnings.catch_warnings(record=True) as w:
            dumped1 = jsons.dump(c)

            # Note: in Python3.5 we cannot be sure that dumped1 contains x,
            # because of the unpredictable order of dicts.

            self.assertTrue('y' not in dumped1)
            warn_msg = w[0].message.args[0]
            self.assertTrue('y' in warn_msg)
            self.assertTrue('Told you so' in warn_msg)

        with self.assertRaises(SerializationError):
            jsons.dump(c, strict=True)

        try:
            jsons.dump(c, strict=True)
        except SerializationError as err:
            self.assertTrue('y' in err.message)
            self.assertTrue('Told you so' in err.message)

    def test_dump_object_with_str_hint(self):
        class C:
            def __init__(self, x: 'str'):
                self.x = x

        dumped = jsons.dump(C('test'), cls=C)

        self.assertDictEqual({'x': 'test'}, dumped)


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
