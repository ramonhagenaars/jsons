from enum import EnumMeta


def default_enum_serializer(obj: EnumMeta,
                            *,
                            use_enum_name: bool = True,
                            **_) -> str:
    """
    Serialize the given obj. By default, the name of the enum element is
    returned.
    :param obj: an instance of an enum.
    :param use_enum_name: determines whether the name or the value should be
    used for serialization.
    :param _: not used.
    :return: ``obj`` serialized as a string.
    """
    attr = 'name' if use_enum_name else 'value'
    return getattr(obj, attr)
