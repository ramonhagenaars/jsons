"""
PRIVATE MODULE: do not import (from) it directly.

This module contains the implementation of ``fork()``.
"""
from typing import Type, Optional

from jsons._common_impl import StateHolder, get_class_name, T


def fork(
        fork_inst: Type[T] = StateHolder,
        name: Optional[str] = None) -> Type[T]:
    """
    Fork from the given ``StateHolder`` to create a separate "branch" of
    serializers and deserializers.
    :param fork_inst: The ``StateHolder`` on which the new fork is based.
    :param name: The ``__name__`` of the new ``type``.
    :return: A "fork inst" that can be used to separately store
    (de)serializers from the regular ``StateHolder``.
    """
    fork_inst._fork_counter += 1
    if name:
        class_name = name
    else:
        class_name = '{}_fork{}'.format(
            get_class_name(fork_inst),
            fork_inst._fork_counter
        )
    result = type(class_name, (fork_inst,), {})
    result._classes_serializers = fork_inst._classes_serializers.copy()
    result._classes_deserializers = fork_inst._classes_deserializers.copy()
    result._serializers = fork_inst._serializers.copy()
    result._deserializers = fork_inst._deserializers.copy()
    result._fork_counter = 0
    result._suppress_warnings = fork_inst._suppress_warnings
    result._suppressed_warnings = fork_inst._suppressed_warnings.copy()
    return result
