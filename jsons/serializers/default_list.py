from collections.abc import Iterable
from typing import Optional

from typish import get_args

from jsons import get_serializer
from jsons._common_impl import StateHolder
from jsons._dump_impl import dump


def default_list_serializer(
        obj: Iterable,
        cls: type = None,
        *,
        strict: bool = False,
        fork_inst: Optional[type] = StateHolder,
        **kwargs) -> list:
    """
    Serialize the given ``obj`` to a list of serialized objects.  fixme: nalopen
    :param obj: the iterable that is to be serialized.
    :param cls: the (subscripted) type of the iterable.
    :param strict: a bool to determine if the serializer should be strict
    (i.e. only dumping stuff that is known to ``cls``).
    :param tasks: the allowed number of tasks (threads or processes).
    :param task_type: the type that is used for multitasking.
    :param kwargs: any keyword arguments that may be given to the serialization
    process.
    :return: a list of which all elements are serialized.
    """
    if not obj:
        return []

    kwargs_ = {**kwargs, 'strict': strict}

    # The meta kwarg store_cls is filtered out, because an iterable should have
    # its own -meta attribute.
    kwargs_.pop('_store_cls', None)

    inner_type = None
    serializer = dump

    cls_args = get_args(cls)
    if cls_args:
        inner_type = cls_args[0]
        serializer = get_serializer(inner_type, fork_inst)
    elif strict:
        inner_type = type(obj[0])
        serializer = get_serializer(inner_type, fork_inst)

    return [serializer(elem, cls=inner_type, fork_inst=fork_inst, **kwargs_) for elem in obj]
