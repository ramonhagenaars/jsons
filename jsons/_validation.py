"""
PRIVATE MODULE: do not import (from) it directly.

This module contains functionality for validating objects.
"""
from typing import Union, Sequence, Callable

from jsons._cache import cached
from jsons._common_impl import StateHolder, get_class_name
from jsons._lizers_impl import _get_lizer
from jsons.exceptions import ValidationError


def set_validator(
        func: Callable[[object], bool],
        cls: Union[type, Sequence[type]],
        *,
        fork_inst: type = StateHolder) -> None:
    """
    Set a validator function for the given ``cls``. The function should accept
    an instance of the type it should validate and must return ``False`` or
    raise any exception in case of a validation failure.
    :param func: the function that takes an instance of type ``cls`` and
    returns a bool (``True`` if the validation was successful).
    :param cls: the type or types that ``func`` is able to validate.
    :param fork_inst: if given, it uses this fork of ``JsonSerializable``.
    :return: None.
    """
    if isinstance(cls, Sequence):
        for cls_ in cls:
            set_validator(func, cls=cls_, fork_inst=fork_inst)
    else:
        cls_name = get_class_name(cls, fully_qualified=True)
        fork_inst._validators[cls_name.lower()] = func
        fork_inst._classes_validators.append(cls)


@cached
def get_validator(
        cls: type,
        fork_inst: type = StateHolder) -> callable:
    """
    Return the validator function that would be used for the given ``cls``.
    :param cls: the type for which a deserializer is to be returned.
    :param fork_inst: if given, it uses this fork of ``JsonSerializable``.
    :return: a validator function.
    """
    return _get_lizer(cls, fork_inst._validators,
                      fork_inst._classes_validators, fork_inst)


def validate(
        obj: object,
        cls: type,
        fork_inst: type = StateHolder) -> None:
    """
    Validate the given ``obj`` with the validator that was registered for
    ``cls``. Raises a ``ValidationError`` if the validation failed.
    :param obj: the object that is to be validated.
    :param cls: the type of which the validator function was registered.
    :param fork_inst: if given, it uses this fork of ``JsonSerializable``.
    :return: None.
    """
    validator = get_validator(cls, fork_inst)
    result = True
    msg = 'Validation failed.'
    if validator:
        try:
            result = validator(obj)
        except Exception as err:
            if err.args:
                msg = err.args[0]
            result = False
    if not result:
        raise ValidationError(msg)
