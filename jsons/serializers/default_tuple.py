from jsons.serializers.default_iterable import default_iterable_serializer


def default_tuple_serializer(obj: tuple, **kwargs) -> list:
    """
    Serialize the given ``obj`` to a list of serialized objects.
    :param obj: the tuple that is to be serialized.
    :param kwargs: any keyword arguments that may be given to the serialization
    process.
    :return: a list of which all elements are serialized.
    """
    return default_iterable_serializer(obj, **kwargs)
