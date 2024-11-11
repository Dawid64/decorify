"""
Module containing general purpose decorators.
"""

from functools import wraps
import multiprocessing
from typing import Any, Callable, Dict
from time import perf_counter
from itertools import product
from .base import decorator


@decorator
def timeit(func: Callable[[Any], Any], accuracy: int = 2) -> Callable[[Any], Any]:
    """
    Decorator for measuring execution time of a function.

    Parameters
    ----------       
    accuracy : int
        Rounding place of the value.

    Returns
    -------
    function
        Wrapped function that returns a tuple of original function's result and
        measured execution time.
    """
    @wraps(func)
    def inner_func(*args, **kwargs):
        start_time = perf_counter()
        result = func(*args, **kwargs)
        execution_time = round(perf_counter() - start_time, accuracy)
        return result, execution_time
    return inner_func


@decorator
def grid_search(func: Callable[[Any], Any], argument_parameters: Dict[str, list],
                return_all_values: bool = False, key=max, return_without_arguments: bool = False) -> Callable[[Any], Any]:
    """ Perfomes the grid search on passed arguments.
    The function can either return found arguments and it's value,
    only value or dictionary of all search aruments and it's values.

    Parameters
    ----------       
    argument_parameters : int
        Rounding place of the value.
    return_all_values: bool
        If True wrapped function returns dictionary {Parameters:value}
    key: Callable, default=max
        Performes following function to find specific value
    return_without_arguments: bool
        Returns only found value

    Returns
    -------
    function
        Wrapped function that returns a tuple of found arguments and
        their value for function.
    """
    @wraps(func)
    def inner_func(*args, **kwargs):
        results = {}
        for values in product(*argument_parameters.values()):
            parameters = dict(zip(argument_parameters.keys(), values))
            results[values] = func(*args, **kwargs, **parameters)
        if return_all_values:
            return results
        best_arguments = key(results, key=lambda val: results[val])
        if return_without_arguments:
            return results[best_arguments]
        return (best_arguments, results[best_arguments])
    return inner_func


@decorator
def time_restriction(func: Callable[[Any], Any], time: float) -> Callable[[Any], Any]:
    """
    A decorator that restricts the execution time of a function. If the function does not complete
    within the specified time limit, it is terminated and a TimeoutError is raised.

    Args:
        func (Callable[[Any], Any]): The function to be decorated.
        time (float): The maximum allowed time for the function to execute, in seconds.

    Returns:
        Callable[[Any], Any]: The wrapped function with time restriction applied.
    """

    @wraps(func)
    def inner_func(*args, **kwargs):
        # system dependent
        multiprocessing.set_start_method('fork', force=True)
        queue = multiprocessing.Queue()

        def worker(func, args, kwargs, queue):
            result = func(*args, **kwargs)
            queue.put(result)

        func_thread = multiprocessing.Process(target=worker, args=(func, args, kwargs, queue))
        func_thread.start()
        func_thread.join(time)
        if func_thread.is_alive():
            func_thread.terminate()
            raise TimeoutError(f"Function {func.__name__} has not finished within the time constraint.")
        return queue.get()
    return inner_func
