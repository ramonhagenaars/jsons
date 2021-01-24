from typing import Optional

from jsons.exceptions import SerializationError


def default_primitive_serializer(obj: object,
                                 cls: Optional[type] = None,
                                 **kwargs) -> object:
    """
    Serialize a primitive; simply return the given ``obj``.
    :param obj: the primitive.
    :param cls: the type of ``obj``.
    :return: ``obj``.
    """
    result = obj
    if cls and obj is not None and not isinstance(obj, cls):
        try:
            result = cls(obj)
        except ValueError as err:
            raise SerializationError('Could not cast "{}" into "{}"'
                                     .format(obj, cls.__name__)) from err
    return result
