from typing import Optional

from jsons.exceptions import DeserializationError


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
    if obj is not None:
        raise DeserializationError('Cannot deserialize {} as NoneType'
                                   .format(obj), source=obj, target=cls)
    return obj
