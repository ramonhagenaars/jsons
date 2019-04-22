from enum import EnumMeta
from typing import Optional


def default_enum_deserializer(obj: str,
                              cls: EnumMeta,
                              *,
                              use_enum_name: Optional[bool] = None,
                              **kwargs) -> object:
    """
    Deserialize an enum value to an enum instance. The serialized value can be
    either the name or the key of an enum entry. If ``use_enum_name`` is set to
    ``True``, then the value *must* be the key of the enum entry. If
    ``use_enum_name`` is set to ``False``, the value *must* be the value of the
    enum entry. By default, this deserializer tries both.
    :param obj: the serialized enum.
    :param cls: the enum class.
    :param use_enum_name: determines whether the name or the value of an enum
    element should be used.
    :param kwargs: not used.
    :return: the corresponding enum element instance.
    """
    if use_enum_name:
        result = cls[obj]
    elif use_enum_name is False:
        result = cls(obj)
    else:  # use_enum_name is None
        try:
            result = cls[obj]
        except KeyError:
            result = cls(obj)  # May raise a ValueError (which is expected).
    return result
