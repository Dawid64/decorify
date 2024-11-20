import os
import sys
from io import TextIOBase
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


def __redirect_dest(file: TextIOBase|str|None) -> TextIOBase:
    """ Returns a file-like object to redirect stdout to."""
    if file is None:
        return open(os.devnull, 'w')
    elif isinstance(file, str):
        return open(file, 'a')
    elif isinstance(file, TextIOBase):
        return file
    raise ValueError("Invalid file type. Please pass a file-like object, a string or None.")


@decorator
def redirect_stdout(file: TextIOBase|str|None = None,__func__: Callable[[Any], Any] = None) -> Callable[[Any], Any]:
    """ Decorator that redirects everything written to stdout to a file or a file-like object.

    Parameters
    ----------
    file : TextIOBase, str, None
        File or file-like object to redirect stdout to. If a string is passed the stdout is redirected
        to a file with that name in append mode. If None, all text written to stdout is deleted instead.

    Returns
    -------
    function
        Wrapped function that has stdout redirected to the specified file.
    """
    @wraps(__func__)
    def inner_func(*args, **kwargs):
        dest = __redirect_dest(file)
        temp_stdout = sys.stdout
        sys.stdout = dest
        result = __func__(*args, **kwargs)
        sys.stdout = temp_stdout
        if dest != file:
            dest.close()
        return result
    return inner_func