from collections.abc import Iterable
from typing import Tuple

from typish import get_args

from jsons._dump_impl import dump
from jsons.exceptions import SerializationError


def default_iterable_serializer(
        obj: Iterable,
        cls: type = None,
        *,
        strict: bool = False,
        **kwargs) -> list:
    """
    Serialize the given ``obj`` to a list of serialized objects.
    :param obj: the iterable that is to be serialized.
    :param cls: the (subscripted) type of the iterable.
    :param strict: a bool to determine if the serializer should be strict
    (i.e. only dumping stuff that is known to ``cls``).
    :param kwargs: any keyword arguments that may be given to the serialization
    process.
    :return: a list of which all elements are serialized.
    """
    # The meta kwarg store_cls is filtered out, because an iterable should have
    # its own -meta attribute.
    kwargs_ = {**kwargs, 'strict': strict}
    kwargs_.pop('_store_cls', None)
    if strict:
        subclasses = _get_subclasses(obj, cls)
    else:
        subclasses = _get_subclasses(obj, None)
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
