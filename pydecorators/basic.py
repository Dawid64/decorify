"""
file.py
"""

from functools import wraps
from typing import Any, Callable
from time import perf_counter

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
