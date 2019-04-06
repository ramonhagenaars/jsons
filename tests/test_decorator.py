import asyncio
from unittest import TestCase
import jsons
from jsons import InvalidDecorationError
from jsons.decorators import loaded, dumped


class TestDecorator(TestCase):
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

    def test_loaded_wrong_dumper(self):
        with self.assertRaises(InvalidDecorationError):
            @dumped(dumper='anything')
            def func():
                pass

    def test_loaded_wrong_loader(self):
        with self.assertRaises(InvalidDecorationError):
            @loaded(loader='anything')
            def func():
                pass
