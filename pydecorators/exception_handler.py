""" Python module for exception handling and validation """
from typing import Callable, Optional
from .base import decorator
from functools import wraps
import logging
import inspect


@decorator
def exception_handling_default_value(func: Callable, default_value=None, *, logger: Optional[logging.Logger] = None):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # TODO
            if isinstance(logger, logging.Logger):
                logger.warning(f"Set default value in function '{
                               func.__name__}', because of '{e}'")
            return default_value

    return wrapper


@decorator
def validate_typehints(func: Callable):
    """ Checks if arguments passed to wrapped functions, are instances of typehint classes
    If not raises Value error.
    Decorator does not change the return value, it's recommended if it's important to check correctness of given types.

    **!! Be aware that this may increase the function runtime. Not recommended for very simple functions. !!**

    Raises
    -------
    Value Error:
        Raises value error if passed arguments does not match the typehints.

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        all_arguments = dict(zip(inspect.getfullargspec(func).args, args))
        all_arguments.update(kwargs)
        for arg, anottation in func.__annotations__.items():
            if arg in all_arguments:
                if not isinstance(all_arguments[arg], anottation):
                    raise ValueError(f"""Expected <{anottation.__name__}> on argument "{arg}", got <{
                                     all_arguments[arg].__class__.__name__}> instead""")
        return func(*args, **kwargs)
    return wrapper
