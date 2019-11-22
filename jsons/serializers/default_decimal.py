from decimal import Decimal


def default_decimal_serializer(obj: Decimal, **kwargs) -> str:
    """
    Serialize a Decimal.
    :param obj: an instance of a Decimal.
    :param kwargs: any keyword arguments.
    :return: ``obj`` serialized as a string.
    """
    return str(obj)
