from typing import Optional, Any

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

    cls_ = cls
    if _is_newtype(cls):
        cls_ = cls.__supertype__

    if cls_ and obj is not None and not isinstance(obj, cls_):
        try:
            result = cls_(obj)
        except ValueError as err:
            raise SerializationError('Could not cast "{}" into "{}"'
                                     .format(obj, cls_.__name__)) from err
    return result


def _is_newtype(cls: Any) -> bool:
    # isinstance(cls, NewType) only works as of Python3.10.
    return hasattr(cls, '__supertype__') and 'NewType' in str(cls)
