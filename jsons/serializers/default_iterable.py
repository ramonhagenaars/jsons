from jsons._main_impl import dump


def default_iterable_serializer(obj: object, **kwargs) -> list:
    """
    Serialize the given ``obj`` to a list of serialized objects.
    :param obj: the iterable that is to be serialized.
    :param kwargs: any keyword arguments that may be given to the serialization
    process.
    :return: a list of which all elements are serialized.
    """
    return [dump(elem, **kwargs) for elem in obj]
