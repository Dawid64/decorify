import os
import sys
from io import IOBase
from functools import wraps
from typing import Any, Callable, Union
from .base import decorator

@decorator
def mute(__func__: Callable[[Any], Any] = None) -> Callable[[Any], Any]:
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


def __redirect_dest(file: Union[IOBase, str, None]) -> IOBase:
    """ Returns a file-like object to redirect stdout to."""
    if file is None:
        return open(os.devnull, 'w')
    elif isinstance(file, str):
        return open(file, 'a')
    elif isinstance(file, IOBase):
        return file
    raise ValueError("Invalid file type. Please pass a file-like object, a string or None.")


@decorator
def redirect(stdout_target: Union[IOBase, str, None] = sys.stdout, stderr_target: Union[IOBase, str, None] = sys.stderr,
    __func__: Callable[[Any], Any] = None, ) -> Callable[[Any], Any]:
    """ Decorator that redirects everything written to stdout to a file or a file-like object.

    Parameters
    ----------
    stdout_target : IOBase, str, None
        File or file-like object to redirect stdout to. If a string is passed the stdout is redirected
        to a file with that name in append mode. If None, all text written to stdout is deleted instead.

        By default no redirection is done.
    stderr_target : IOBase, str, None
        File or file-like object to redirect stderr to. If a string is passed the stdout is redirected
        to a file with that name in append mode. If None, all text written to stdout is deleted instead.
        
        By default no redirection is done.
    
    Returns
    -------
    function
        Wrapped function that has stdout and stderr redirected to the specified file.
    """
    @wraps(__func__)
    def inner_func(*args, **kwargs):
        dest_stdout = __redirect_dest(stdout_target)
        dest_stderr = __redirect_dest(stderr_target)
        temp_stdout = sys.stdout
        temp_stderr = sys.stderr
        sys.stdout = dest_stdout
        sys.stderr = dest_stderr
        result = __func__(*args, **kwargs)
        sys.stdout = temp_stdout
        sys.stderr = temp_stderr
        if dest_stdout != stdout_target:
            dest_stdout.close()
        if dest_stderr != stderr_target:
            dest_stderr.close()
        return result
    return inner_func
