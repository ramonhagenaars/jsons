from multiprocessing import Process, Manager
from typish import get_args
from jsons._load_impl import load
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
        result = _single_task(obj, cls_, **kwargs_)
    elif tasks > 1:
        result = _multi_task(obj, cls_, tasks, task_type, **kwargs_)
    else:
        raise JsonsError('Invalid number of tasks: {}'.format(tasks))
    return result


def _single_task(
        # Load the elements of the list in a single task.
        obj: list,
        cls: type,
        **kwargs):
    return [load(x, cls, tasks=1, **kwargs) for x in obj]


def _multi_task(
        obj: list,
        cls: type,
        tasks: int,
        task_type: type,
        **kwargs):
    # Load the elements of the list with multiple tasks.

    # First, create a list with the correct size for the tasks to fill.
    if issubclass(task_type, Process):
        manager = Manager()
        result = manager.list([0] * len(obj))
    else:
        result = [0] * len(obj)

    tasks_used = min(tasks, len(obj))
    tasks_left = tasks - tasks_used or 1

    # Divide the list in parts.
    slice_size = int(len(obj) / tasks_used)
    rest_size = len(obj) % tasks_used

    # Start the tasks and store them to join them later.
    tasks_instances = []
    for i in range(tasks_used):
        start = i
        end = (i + 1) * slice_size
        if i == tasks_used - 1:
            end += rest_size
        task = task_type(
            target=_fill,
            args=(obj, cls, result, start, end, tasks_left, kwargs))
        task.start()
        tasks_instances.append(task)

    for task in tasks_instances:
        task.join()

    return list(result)


def _fill(
        obj: list,
        cls: type,
        result: list,
        start: int,
        end: int,
        tasks: int,
        kwargs: dict):
    # Fill result with the loaded objects of obj within the range start - end.
    for i_ in range(start, end):
        loaded = load(obj[i_], cls, tasks=tasks, **kwargs)
        result[i_] = loaded
