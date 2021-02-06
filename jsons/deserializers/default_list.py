from multiprocessing import Process
from typing import Type

from typish import get_args

from jsons._common_impl import StateHolder
from jsons._load_impl import load
from jsons._multitasking import multi_task
from jsons.exceptions import JsonsError, DeserializationError


def default_list_deserializer(
        obj: list,
        cls: type = None,
        *,
        warn_on_fail: bool = False,
        tasks: int = 1,
        task_type: type = Process,
        fork_inst: Type[StateHolder] = StateHolder,
        **kwargs) -> list:
    """
    Deserialize a list by deserializing all items of that list.
    :param obj: the list that needs deserializing.
    :param cls: the type optionally with a generic (e.g. List[str]).
    :param warn_on_fail: if ``True``, will warn upon any failure and continue.
    :param tasks: the allowed number of tasks (threads or processes).
    :param task_type: the type that is used for multitasking.
    :param fork_inst: if given, it uses this fork of ``JsonSerializable``.
    :param kwargs: any keyword arguments.
    :return: a deserialized list instance.
    """
    cls_ = None
    kwargs_ = {**kwargs}
    cls_args = get_args(cls)
    if cls_args:
        cls_ = cls_args[0]
        # Mark the cls as 'inferred' so that later it is known where cls came
        # from and the precedence of classes can be determined.
        kwargs_['_inferred_cls'] = True

    if tasks == 1:
        result = _do_load(obj, cls_, warn_on_fail, fork_inst, kwargs_)
    elif tasks > 1:
        result = multi_task(load, obj, tasks, task_type, cls_, **kwargs_)
    else:
        raise JsonsError('Invalid number of tasks: {}'.format(tasks))
    return result


def _do_load(
        obj: list,
        cls: type,
        warn_on_fail: bool,
        fork_inst: Type[StateHolder],
        kwargs) -> list:
    result = []
    for index, elem in enumerate(obj):
        try:
            result.append(load(elem, cls=cls, tasks=1, **kwargs))
        except DeserializationError as err:
            new_msg = ('Could not deserialize element at index %s. %s' %
                       (index, err.message))
            if warn_on_fail:
                fork_inst._warn(new_msg, 'element-not-deserialized')
            else:
                new_err = DeserializationError(new_msg, err.source, err.target)
                raise new_err from err

    return result
