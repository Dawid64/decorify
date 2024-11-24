"""
Module containing general purpose decorators.
"""

from ast import List
from functools import wraps
import multiprocessing
from typing import Any, Callable, Dict
from time import perf_counter
from itertools import product
from .base import decorator
from multiprocessing.pool import ThreadPool
from multiprocessing.context import TimeoutError as mp_TimeoutError
from time import time as get_time
from time import sleep


@decorator
def timeit(accuracy: int = 2, __func__: Callable[[Any], Any] = None) -> Callable[[Any], Any]:
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
    @wraps(__func__)
    def inner_func(*args, **kwargs):
        start_time = perf_counter()
        result = __func__(*args, **kwargs)
        execution_time = round(perf_counter() - start_time, accuracy)
        return result, execution_time
    return inner_func


@decorator
def grid_search(argument_parameters: Dict[str, list],
                return_all_values: bool = False, key=max, return_without_arguments: bool = False,
                __func__: Callable[[Any], Any] = None) -> Callable[[Any], Any]:
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
    @wraps(__func__)
    def inner_func(*args, **kwargs):
        results = {}
        for values in product(*argument_parameters.values()):
            parameters = dict(zip(argument_parameters.keys(), values))
            results[values] = __func__(*args, **kwargs, **parameters)
        if return_all_values:
            return results
        best_arguments = key(results, key=lambda val: results[val])
        if return_without_arguments:
            return results[best_arguments]
        return (best_arguments, results[best_arguments])
    return inner_func


@decorator
def timeout(time: float, default_value: Any = mp_TimeoutError, __func__=None) -> Callable[[Any], Any]:
    """ Decorated function is run in new process while still sharing memory, if the time limit is reached
    function returns default value or raises TimeoutError if default_value is not set.

    **!!Note function uses multiprocessing library which does not provide support for IOS, Android and WASI!!**

    ## Args:
        time (float): timeout limit in seconds.
        default_value (Any, optional): value to be outputted if timeout is reached. Defaults to mp_TimeoutError.

    ## Raises:
        TimeoutError: if time limit is reached

    ## Wrapped Function Returns:
        Functions output if function reached in time limit or default value if such value was set, and time limit was reached
    """
    @wraps(__func__)
    def wrapped(*args, **kwargs):
        with ThreadPool(1) as pool:
            res = pool.apply_async(__func__, args, kwargs)
            try:
                result = res.get(timeout=time)
            except mp_TimeoutError:
                if default_value is not mp_TimeoutError:
                    return default_value
                raise TimeoutError()
        return result
    return wrapped


@decorator
def limitter(time: float, max_calls: int, __func__=None) -> Callable[[Any], Any]:
    __func__.__calls = []

    @wraps(__func__)
    def wrapped(*args, **kwargs):
        current_time = get_time()

        def _calc(call):
            return current_time - call < time

        def _filter(calls):
            return list(filter(_calc, calls))

        __func__.__calls = _filter(__func__.__calls)

        if len(__func__.__calls) >= max_calls:
            sleep(__func__.__calls[0] + time - current_time)

        __func__.__calls.append(current_time)
        return __func__(*args, **kwargs)
    return wrapped
