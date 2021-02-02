from typing import Optional

from jsons.exceptions import DeserializationError


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
    result = obj
    if obj is not None and not isinstance(obj, cls):
        try:
            result = cls(obj)
        except ValueError as err:
            raise DeserializationError(
                'Could not cast "{}" into "{}"'.format(obj, cls.__name__),
                obj, cls) from err
    return result
