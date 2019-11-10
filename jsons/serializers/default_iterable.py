from collections.abc import Iterable
from typing import Tuple

from typish import get_args

from jsons._dump_impl import dump
from jsons.exceptions import SerializationError


def default_iterable_serializer(
        obj: Iterable,
        cls: type = None,
        **kwargs) -> list:
    """
    Serialize the given ``obj`` to a list of serialized objects.
    :param obj: the iterable that is to be serialized.
    :param cls: the (subscripted) type of the iterable.
    :param kwargs: any keyword arguments that may be given to the serialization
    process.
    :return: a list of which all elements are serialized.
    """
    # The meta kwarg store_cls is filtered out, because an iterable should have
    # its own -meta attribute.
    kwargs_ = {key: kwargs[key] for key in kwargs if key != '_store_cls'}
    subclasses = _get_subclasses(obj, cls)
    return [dump(elem, cls=subclasses[i], **kwargs_)
            for i, elem in enumerate(obj)]


def _get_subclasses(obj: Iterable, cls: type = None) -> Tuple[type, ...]:
    subclasses = (None,) * len(obj)
    if cls:
        args = get_args(cls)
        if len(args) == 1:
            # E.g. List[int]
            subclasses = args * len(obj)
        elif len(args) > 1:
            # E.g. Tuple[int, str, str]
            subclasses = args
    if len(subclasses) != len(obj):
        msg = ('Not enough generic types ({}) in {}, expected {} to match '
               'the iterable of length {}'
               .format(len(subclasses), cls, len(obj), len(obj)))
        raise SerializationError(msg)
    return subclasses
