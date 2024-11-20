from functools import wraps
from typing import Any, Callable
from .base import decorator

@decorator
def no_print(__func__: Callable[[Any], Any] = None) -> Callable[[Any], Any]:
    """ Decorator that disables ALL print statements in decorated function and its nested functions.
    
    Returns
    -------
    function
        Wrapped function that has ALL print statements disabled.
    """
    @wraps(__func__)
    def inner_func(*args, **kwargs):
        temp_print = __builtins__["print"]
        __builtins__["print"] = lambda *args, **kwargs: None
        result = __func__(*args, **kwargs)
        __builtins__["print"] = temp_print
        return result
    return inner_func