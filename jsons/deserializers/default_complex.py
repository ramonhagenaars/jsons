from typing import Dict


def default_complex_deserializer(obj: Dict[str, float],
                                 cls: type = complex,
                                 **kwargs) -> complex:
    """
    Deserialize a dictionary with 'real' and 'imag' keys to a complex number.
    :param obj: the dict that is to be deserialized.
    :param cls: not used.
    :param kwargs: not used.
    :return: an instance of ``complex``.
    """
    real = obj.get('real')
    imag = obj.get('imag')
    clean_obj = {'real': real, 'imag': imag}
    for key, value in clean_obj.items():
        if not value:
            raise AttributeError("Cannot deserialize {} to a complex number, does not contain key '{}'".format(obj, key))
        try:
            float(value)
        except TypeError:
            raise AttributeError("Cannot deserialize {} to a complex number, can't cast value of '{}' to float".format(obj, key))

    return complex(real, imag)
