from jsons.serializers.default_iterable import default_iterable_serializer


def default_list_serializer(obj: list, **kwargs) -> list:
    """
    Serialize the given ``obj`` to a list of serialized objects.
    :param obj: the list that is to be serialized.
    :param kwargs: any keyword arguments that may be given to the serialization
    process.
    :return: a list of which all elements are serialized.
    """
    return default_iterable_serializer(obj, **kwargs)
