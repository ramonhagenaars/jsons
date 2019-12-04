def default_complex_serializer(obj: complex, **_) -> dict:
    """
    Serialize a complex as a dict.
    :param obj: the complex.
    :param _: not used.
    :return: a ``dict``.
    """
    return {'real': obj.real, 'imag': obj.imag}
