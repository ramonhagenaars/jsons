from multiprocessing import Process

from typish import get_args

from jsons._load_impl import load
from jsons._multitasking import multi_task
from jsons.exceptions import JsonsError


def default_list_deserializer(
        obj: list,
        cls: type = None,
        *,
        tasks: int = 1,
        task_type: type = Process,
        **kwargs) -> list:
    """
    Deserialize a list by deserializing all items of that list.
    :param obj: the list that needs deserializing.
    :param cls: the type optionally with a generic (e.g. List[str]).
    :param tasks: the allowed number of tasks (threads or processes).
    :param task_type: the type that is used for multitasking.
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
        result = [load(elem, cls=cls_, tasks=1, **kwargs_) for elem in obj]
    elif tasks > 1:
        result = multi_task(load, obj, tasks, task_type, cls_, **kwargs_)
    else:
        raise JsonsError('Invalid number of tasks: {}'.format(tasks))
    return result
