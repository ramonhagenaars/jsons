from typing import Literal, Any

from jsons._dump_impl import dump

def default_literal_serializer(obj: Any, cls: Literal, **kwargs):
    return dump(obj, type(obj), **kwargs)
