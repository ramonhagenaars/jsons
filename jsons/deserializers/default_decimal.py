from decimal import Decimal
from typing import Optional, Union


def default_decimal_deserializer(obj: Union[str, float, int],
                                 cls: Optional[type] = None,
                                 **kwargs) -> Decimal:
    """
    Deserialize a Decimal. Expects a string representation of a number, or
    the number itself as a float or int.
    :param obj: the string float or int that is to be deserialized.
    :param cls: not used.
    :param kwargs: any keyword arguments.
    :return: the deserialized obj.
    """
    return Decimal(obj)
