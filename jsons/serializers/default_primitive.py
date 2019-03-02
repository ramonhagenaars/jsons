def default_primitive_serializer(obj: object, **_) -> object:
    """
    Serialize a primitive; simply return the given ``obj``.
    :param obj: the primitive.
    :param _: not used.
    :return: ``obj``.
    """
    return obj
