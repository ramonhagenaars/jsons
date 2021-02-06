"""
PRIVATE MODULE: do not import (from) it directly.

This module contains implementations that do not directly touch the core of
jsons.
"""
from typing import Optional

from jsons._cache import cached
from jsons._common_impl import StateHolder, get_class_name


def suppress_warnings(
        do_suppress: Optional[bool] = True,
        fork_inst: Optional[type] = StateHolder):
    """
    Suppress (or stop suppressing) warnings altogether.
    :param do_suppress: if ``True``, warnings will be suppressed from now on.
    :param fork_inst: if given, it uses this fork of ``JsonSerializable``.
    :return: None.
    """
    fork_inst._suppress_warnings = do_suppress


def suppress_warning(
        code: str,
        fork_inst: Optional[type] = StateHolder):
    """
    Suppress a specific warning that corresponds to the given code (see the
    warning).
    :param code: the code of the warning that is to be suppressed.
    :param fork_inst: if given, it uses this fork of ``JsonSerializable``.
    :return: None.
    """
    fork_inst._suppressed_warnings |= {code}


@cached
def announce_class(
        cls: type,
        cls_name: Optional[str] = None,
        fork_inst: type = StateHolder):
    """
    Announce the given cls to jsons to allow jsons to deserialize a verbose
    dump into that class.
    :param cls: the class that is to be announced.
    :param cls_name: a custom name for that class.
    :param fork_inst: if given, it uses this fork of ``JsonSerializable``.
    :return: None.
    """
    cls_name = cls_name or get_class_name(cls, fully_qualified=True)
    fork_inst._announced_classes[cls] = cls_name
    fork_inst._announced_classes[cls_name] = cls
