from unittest import TestCase

import jsons
from jsons import (
    camelcase,
    snakecase,
    pascalcase,
    lispcase
)


class TestCaseTransformer(TestCase):
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
