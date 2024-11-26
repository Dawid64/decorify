import os
import sys
import builtins
from io import IOBase
from functools import wraps
from typing import Any, Callable, Union, Literal
from .base import decorator

@decorator
def mute(level: Literal["print", "stdout", "warning"] = "print", __func__: Callable[[Any], Any] = None) -> Callable[[Any], Any]:
    """ Decorator that disables some or all writes to stdout and/or stderr in decorated function and its nested functions.
    
    Parameters
    ----------
    level : Literal["print", "stdout", "warning", "error"]
        Specifies the type of text to mute. The following options are available:
        - "print": Disables all print statements.
        - "stdout": Disables all text written to stdout.
        - "warning": Disables all text written to stdout and stderr except Exceptions.

    Returns
    -------
    function
        Wrapped function that has ALL print statements and optionally all other text written to stdout disabled.
    """
    @wraps(__func__)
    def inner_func(*args, **kwargs):
        if level == "print":
            temp_print = builtins.print
            builtins.print = lambda *args, **kwargs: None
            result = __func__(*args, **kwargs)
            builtins.print = temp_print
        elif level == "stdout":
            result = redirect(stdout_target=None)(__func__)(*args, **kwargs)
        elif level == "warning":
            try:
                result = redirect(stdout_target=None, stderr_target=None, exclude_errors=True)(__func__)(*args, **kwargs)
            except Exception as e:
                result = None
                raise e
        else:
            raise ValueError("Invalid level. Please pass 'print', 'stdout' or 'warning'.")
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
    exclude_errors: bool = False, __func__: Callable[[Any], Any] = None, ) -> Callable[[Any], Any]:
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
    exclude_errors : bool
        If True, exceptions raised in the decorated function will not be redirected alongside the rest of stderr.
        By default all exceptions are written to the stderr_target.

    
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
        try:
            result = __func__(*args, **kwargs)
        finally:
            if exclude_errors:
                sys.stderr = temp_stderr
        sys.stdout = temp_stdout
        sys.stderr = temp_stderr
        if dest_stdout != stdout_target:
            dest_stdout.close()
        if dest_stderr != stderr_target:
            dest_stderr.close()
        return result
    return inner_func
