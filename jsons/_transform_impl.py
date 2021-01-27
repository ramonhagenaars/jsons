"""
PRIVATE MODULE: do not import (from) it directly.

This module contains functionality for loading stuff from json.
"""
from typing import Type, List, Any, Dict, Callable

from jsons._common_impl import T
from jsons._dump_impl import dump
from jsons._load_impl import load


def transform(
        obj: object,
        cls: Type[T],
        *,
        mapper: Callable[[Dict[str, Any]], Dict[str, Any]] = None,
        dump_cls: type = None,
        dump_args: List[Any] = None,
        dump_kwargs: List[Dict[str, Any]] = None,
        **kwargs) -> T:
    """
    Transform the given ``obj`` to an instance of ``cls``.

    :param obj: the object that is to be transformed into a type of ``cls``.
    :param cls: the type that ``obj`` is to be transformed into.
    :param mapper: a callable that takes the dumped dict and returns a mapped
    dict right before it is loaded into ``cls``.
    :param dump_cls: the ``cls`` parameter that is given to ``dump``.
    :param dump_args: the ``args`` parameter that is given to ``dump``.
    :param dump_kwargs: the ``kwargs`` parameter that is given to ``dump``.
    :param kwargs: any keyword arguments that are given to ``load``.
    :return: an instance of ``cls``.
    """
    dump_args_ = dump_args or []
    dump_kwargs_ = dump_kwargs or {}
    dumped = dump(obj, dump_cls, *dump_args_, **dump_kwargs_)
    mapper_ = mapper or (lambda x: x)
    dumped_mapped = mapper_(dumped)
    return load(dumped_mapped, cls, **kwargs)
