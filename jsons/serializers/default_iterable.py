from collections.abc import Iterable
from jsons._dump_impl import dump


def default_iterable_serializer(obj: Iterable, **kwargs) -> list:
    """
    Serialize the given ``obj`` to a list of serialized objects.
    :param obj: the iterable that is to be serialized.
    :param kwargs: any keyword arguments that may be given to the serialization
    process.
    :return: a list of which all elements are serialized.
    """
    # The meta kwarg store_cls is filtered out, because an iterable should have
    # its own -meta attribute.
    kwargs_ = {key: kwargs[key] for key in kwargs if key != '_store_cls'}
    return [dump(elem, **kwargs_) for elem in obj]
