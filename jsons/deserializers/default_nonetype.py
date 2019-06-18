from typing import Optional


def default_nonetype_deserializer(obj: object,
                                  cls: Optional[type] = None,
                                  **kwargs) -> object:
    """
    Deserialize a ``NoneType``.
    :param obj: the value that is to be deserialized.
    :param cls: not used.
    :param kwargs: not used.
    :return: ``obj``.
    """
    return obj
