from typing import Dict

from jsons._load_impl import load
from jsons.exceptions import DeserializationError


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
    try:
        clean_obj = load({'real': obj['real'], 'imag': obj['imag']},
                         cls=Dict[str, float])
        return complex(clean_obj['real'], clean_obj['imag'])
    except KeyError as err:
        raise AttributeError("Cannot deserialize {} to a complex number, "
                             "does not contain key '{}'"
                             .format(obj, err.args[0])) from err
    except DeserializationError as err:
        raise AttributeError("Cannot deserialize {} to a complex number, "
                             "cannot cast value {} to float"
                             .format(obj, err.source)) from err
