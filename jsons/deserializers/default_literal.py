from typing import Literal, Any, get_args

from jsons.exceptions import DeserializationError

def default_literal_deserializer(obj: Any, cls: Literal, *, strictly_equal_literal: bool = False, **kwargs):
    for literal_value in get_args(cls):
        value_equal = obj == literal_value
        type_equal = type(obj) == type(literal_value)
        if value_equal and (not strictly_equal_literal or type_equal):
            break
    else:
        err_msg = 'Could not match the object "{}" to the Literal: {}'.format(obj, cls)
        raise DeserializationError(err_msg, obj, None)
    return literal_value
