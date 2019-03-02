from typing import Optional


def default_primitive_deserializer(obj: object,
                                   cls: Optional[type] = None,
                                   **kwargs) -> object:
    """
    Deserialize a primitive: it simply returns the given primitive.
    :param obj: the value that is to be deserialized.
    :param cls: not used.
    :param kwargs: not used.
    :return: ``obj``.
    """
    return obj
