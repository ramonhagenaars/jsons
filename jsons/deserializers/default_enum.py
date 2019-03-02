from enum import EnumMeta


def default_enum_deserializer(obj: str,
                              cls: EnumMeta,
                              use_enum_name: bool = True,
                              **kwargs) -> object:
    """
    Deserialize an enum value to an enum instance. The serialized value must
    can be the name of the enum element or the value; dependent on
    ``use_enum_name``.
    :param obj: the serialized enum.
    :param cls: the enum class.
    :param use_enum_name: determines whether the name or the value of an enum
    element should be used.
    :param kwargs: not used.
    :return: the corresponding enum element instance.
    """
    return cls[obj] if use_enum_name else cls(obj)
