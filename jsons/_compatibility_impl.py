"""
PRIVATE MODULE: do not import (from) it directly.

This module contains functionality for supporting the compatibility of jsons
with multiple Python versions.
"""
import sys
import typing
from enum import Enum

from jsons._cache import cached


class Flag(Enum):
    """
    This is a light version of the Flag enum type that was introduced in
    Python3.6. It supports the use of pipes for members (Flag.A | Flag.B).
    """

    @classmethod
    def _get_inst(cls, value):
        try:
            result = cls(value)
        except ValueError:
            pseudo_member = object.__new__(cls)
            pseudo_member._value_ = value
            contained = [elem.name for elem in cls if elem in pseudo_member]
            pseudo_member._name_ = '|'.join(contained)
            result = pseudo_member
        return result

    def __or__(self, other: 'Flag') -> 'Flag':
        new_value = other.value | self.value
        return self._get_inst(new_value)

    def __contains__(self, item: 'Flag') -> bool:
        return item.value == self.value & item.value

    __ror__ = __or__


@cached
def tuple_with_ellipsis(tup: type) -> bool:
    # Python3.5: Tuples have __tuple_use_ellipsis__
    # Python3.7: Tuples have __args__
    use_el = getattr(tup, '__tuple_use_ellipsis__', None)
    if use_el is None:
        use_el = tup.__args__[-1] is ...
    return use_el


@cached
def get_union_params(un: type) -> list:
    # Python3.5: Unions have __union_params__
    # Python3.7: Unions have __args__
    return getattr(un, '__union_params__', getattr(un, '__args__', None))


@cached
def get_naked_class(cls: type) -> type:
    # Python3.5: typing classes have __extra__
    # Python3.6: typing classes have __extra__
    # Python3.7: typing classes have __origin__
    # Return the non-generic class (e.g. dict) of a generic type (e.g. Dict).
    return getattr(cls, '__extra__', getattr(cls, '__origin__', cls))


@cached
def get_type_hints(func: callable, fallback_ns=None):
    # Python3.5: get_type_hints raises on classes without explicit constructor
    try:
        result = typing.get_type_hints(func)
    except AttributeError:
        result = {}
    except NameError:
        # attempt to resolve in global namespace - this works around an
        # issue in 3.7 whereby __init__ created by dataclasses fails
        # to find it's context. See https://bugs.python.org/issue34776
        if fallback_ns is not None:
            context_dict = sys.modules[fallback_ns].__dict__
            result = typing.get_type_hints(func, globalns=context_dict)
    return result
