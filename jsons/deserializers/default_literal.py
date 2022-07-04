from typing import Literal, Any, get_args

from jsons.exceptions import DeserializationError

def default_literal_deserializer(obj: Any, cls: Literal, *, strictly_equal_literal: bool = False, **_):
    """
    Deserialize an object to any matching value of the given Literal. The first
    successful deserialization is returned.
    :param obj: The object that needs deserializing.
    :param cls: The Literal type with values (e.g. Literal[1, 2]).
    :param strictly_equal_literal: determines whether the type of the value
    and literal should also be taken into account.
    :param _: not used.
    :return: An object of the first value of the Literal that could be
    deserialized successfully.
    """
    for literal_value in get_args(cls):
        value_equal = obj == literal_value
        type_equal = type(obj) == type(literal_value)
        if value_equal and (not strictly_equal_literal or type_equal):
            break
    else:
        err_msg = 'Could not match the object "{}" to the Literal: {}'.format(obj, cls)
        raise DeserializationError(err_msg, obj, None)
    return literal_value
