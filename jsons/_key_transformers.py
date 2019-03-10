"""
PRIVATE MODULE: do not import (from) it directly.

This module contains functions that can be used to transform keys of
dictionaries.
"""
import re


def camelcase(str_: str) -> str:
    """
    Return ``s`` in camelCase.
    :param str_: the string that is to be transformed.
    :return: a string in camelCase.
    """
    str_ = str_.replace('-', '_')
    splitted = str_.split('_')
    if len(splitted) > 1:
        str_ = ''.join([x.title() for x in splitted])
    return str_[0].lower() + str_[1:]


def snakecase(str_: str) -> str:
    """
    Return ``s`` in snake_case.
    :param str_: the string that is to be transformed.
    :return: a string in snake_case.
    """
    str_ = str_.replace('-', '_')
    str_ = str_[0].lower() + str_[1:]
    return re.sub(r'([a-z])([A-Z])', '\\1_\\2', str_).lower()


def pascalcase(str_: str) -> str:
    """
    Return ``s`` in PascalCase.
    :param str_: the string that is to be transformed.
    :return: a string in PascalCase.
    """
    camelcase_str = camelcase(str_)
    return camelcase_str[0].upper() + camelcase_str[1:]


def lispcase(str_: str) -> str:
    """
    Return ``s`` in lisp-case.
    :param str_: the string that is to be transformed.
    :return: a string in lisp-case.
    """
    return snakecase(str_).replace('_', '-')
