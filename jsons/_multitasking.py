"""
PRIVATE MODULE: do not import (from) it directly.

Functionality for processing iterables in parallel.
"""
from multiprocessing import Process, Manager
from typing import List, Callable, Union

from typish import Something

Subscriptable = Something['__getitem__': Callable[[int], object]]


def multi_task(
        func: Callable,
        obj: Subscriptable,
        tasks: int,
        task_type: type,
        *args,
        **kwargs):
    result = _get_list_to_fill(obj, task_type)
    tasks_instances = _start_tasks(tasks=tasks, task_type=task_type, func=func,
                                   list_to_fill=result, obj=obj, args=args,
                                   kwargs=kwargs)
    for task in tasks_instances:
        task.join()

    return list(result)


def _get_list_to_fill(obj: list, task_type: type) -> Union[list, Manager]:
    # Return a list or manager that contains enough spots to fill.
    result = [0] * len(obj)
    if issubclass(task_type, Process):
        manager = Manager()
        result = manager.list(result)
    return result


def _start_tasks(
        tasks: int,
        task_type: type,
        func: Callable,
        list_to_fill: list,
        obj: Subscriptable,
        args,
        kwargs) -> List[Something['join': Callable[[], None]]]:
    # Start the tasks and return their instances so they can be joined.

    tasks_instances = []
    tasks_used = min(tasks, len(obj))
    tasks_left = tasks - tasks_used or 1

    # Divide the list in parts.
    slice_size = int(len(obj) / tasks_used)
    rest_size = len(obj) % tasks_used
    for i in range(tasks_used):
        start = i * slice_size
        end = (i + 1) * slice_size
        if i == tasks_used - 1:
            end += rest_size
        task = task_type(
            target=_fill,
            args=(func, list_to_fill, obj, start, end, tasks_left, args, kwargs))
        task.start()
        tasks_instances.append(task)
    return tasks_instances


def _fill(
        func,
        list_to_fill: list,
        obj: Subscriptable,
        start: int,
        end: int,
        tasks: int,
        args,
        kwargs):
    # Fill the given list with results from func.
    for i_ in range(start, end):
        loaded = func(obj[i_], tasks=tasks, *args, **kwargs)
        list_to_fill[i_] = loaded
