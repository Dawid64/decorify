"""
Module containing general purpose decorators.
"""

import datetime
from functools import wraps
from typing import Any, Callable, Dict
from time import perf_counter, sleep
from time import time as time_
from itertools import product
from .base import decorator
from multiprocessing.pool import ThreadPool
from multiprocessing.context import TimeoutError as mp_TimeoutError


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
def rate_limiter(time: float, max_calls: int, __func__=None) -> Callable[[Any], Any]:
    """
    A decorator that enforces a rate limit on function calls. The decorated function can only be called a
    specified number of times within a given time interval. If the limit is reached, the function will wait
    until the next allowed call time before proceeding.

    **!!Note that this decorator is not thread-safe and should not be used carefully in a multi-threaded environment!!**

    Parameters
    ----------
    time : float
        The time window in seconds during which the number of function calls is limited.
    max_calls : int
        The maximum number of allowed calls to the function within the specified time window.

    Returns
    -------
    Callable[[Any], Any]
        The wrapped function with rate limiting applied.

    Notes
    -----
    - The decorator uses a simple mechanism to track function call timestamps and enforce the rate limit.
    - When the maximum number of calls is reached within the given time window, the function will wait for
      enough time to allow another call to proceed.
    - This decorator is particularly useful for controlling the rate of expensive operations or API requests.

    Examples
    --------
    >>> from decorify import rate_limiter
    >>> @rate_limiter(time=10, max_calls=2)
    ... def example_function(x):
    ...     print(f"Processing {x}")

    >>> example_function(1)  # Immediate execution
    Processing 1
    >>> example_function(2)  # Immediate execution
    Processing 2
    >>> example_function(3)  # Waits until rate limit allows
    Processing 3
    """
    __func__.__calls = []

    @wraps(__func__)
    def wrapped(*args, **kwargs):
        starting_time = perf_counter()

        def _calc(call):
            return starting_time - call < time

        __func__.__calls = list(filter(_calc, __func__.__calls))

        if len(__func__.__calls) >= max_calls:
            sleep(__func__.__calls[0] + time - starting_time)

        __func__.__calls.append(perf_counter())
        return __func__(*args, **kwargs)
    return wrapped


@decorator
def time_limiter(time: float, max_calls: int, sync_with_clock: bool = False, __func__=None) -> Callable[[Any], Any]:
    """
    A decorator that enforces a time limit on function calls. The decorated function can only be called a
    specified number of times within a given time interval. If the limit is reached, the function will wait
    until the next allowed call time before proceeding. The decorator can also synchronize with the system
    clock and reset the call counter each time interval counting from 00:00:00.
    So for example, if the time interval is 10 minutes, if you execute the function at 6:38, the next call
    will be allowed at 6:48 (or 6:40 if `sync_with_clock` is enabled).

    **!!Note that this decorator is not thread-safe and should not be used carefully in a multi-threaded environment!!**

    Parameters
    ----------
    time : float
        The time window in seconds during which the number of function calls is limited.
    max_calls : int
        The maximum number of allowed calls to the function within the specified time window.
    sync_with_clock : bool, default=False
        If True, the decorator will synchronize with the system clock and reset the call counter each time interval counting from 00:00:00.

    Returns
    -------
    Callable[[Any], Any]
        The wrapped function with time limiting applied.

    Notes
    -----
    - The decorator uses a simple mechanism to track function call timestamps and enforce the rate limit.
    - When the maximum number of calls is reached within the given time window, the function will wait for
      enough time to allow another call to proceed.
    - This decorator is particularly useful for controlling the rate of expensive operations or API requests.

    Examples
    --------
    >>> from decorify import rate_limiter
    >>> @rate_limiter(time=10, max_calls=2)
    ... def example_function(x):
    ...     print(f"Processing {x}")

    >>> example_function(1)  # Immediate execution
    Processing 1
    >>> example_function(2)  # Immediate execution
    Processing 2
    >>> example_function(3)  # Waits until time limit allows
    Processing 3
    """
    if sync_with_clock:
        now = datetime.datetime.now()
        start_time = int(time_()) - (now.hour * 3600 + now.minute * 60 + now.second)
    else:
        start_time = time_()

    __func__.__interval_counter = 0
    __func__.__interval_number = (time_() - start_time) // time

    @wraps(__func__)
    def wrapped(*args, **kwargs):
        current_interval = (time_() - start_time) // time
        if current_interval <= __func__.__interval_number and __func__.__interval_counter >= max_calls:
            sleep(time - ((time_() - start_time) % time))
            current_interval = (time_() - start_time) // time

        if current_interval > __func__.__interval_number:
            __func__.__interval_counter = 0
            __func__.__interval_number = current_interval

        __func__.__interval_counter += 1
        return __func__(*args, **kwargs)

    return wrapped
