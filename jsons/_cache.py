"""
PRIVATE MODULE: do not import (from) it directly.

This module contains functionality for caching functions.
"""
from collections import deque
from functools import lru_cache, update_wrapper
from typing import Callable


class _Wrapper:
    """
    A wrapper around a function that needs to be cached. This wrapper allows
    for a single point from which cache can be cleared.
    """
    instances = deque([])

    def __init__(self, wrapped):
        self.wrapped = wrapped
        self.instances.append(self)

    @lru_cache(typed=True)
    def __call__(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)


def cached(decorated: Callable):
    """
    Alternative for ``functools.lru_cache``. By decorating a function with
    ``cached``, you can clear the cache of that function by calling
    ``clear()``.
    :param decorated: the decorated function.
    :return: a wrapped function.
    """
    wrapper = _Wrapper(decorated)
    update_wrapper(wrapper=wrapper, wrapped=decorated)
    return wrapper


def clear():
    """
    Clear all cache of functions that were cached using ``cached``.
    :return: None.
    """
    for w in _Wrapper.instances:
        w.__call__.cache_clear()
