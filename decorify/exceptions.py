""" Python module for exception handling and validation """
from typing import Any, Callable, Optional
from .base import decorator
from functools import wraps
import logging
import inspect


@decorator
def default_value(default_value: Any = None, *, logger: Optional[logging.Logger] = None, __func__: Callable = None):
    """
    Decorator for assigning default value if function fails

    Parameters
    ----------       
    default_value : Any
        Default value which is set if the funciton fails  
    logger : logging.Logger
        Logger for logging warning if the function failed and the default value was returned

    Returns
    -------
    function
        Wrapped function that returns defealut value if exception is raised
    """
    @wraps(__func__)
    def wrapper(*args, **kwargs):
        try:
            return __func__(*args, **kwargs)
        except Exception as e:
            if isinstance(logger, logging.Logger):
                logger.warning(f"""Set default value in function '{
                               __func__.__name__}', because of '{e}'""")
            return default_value

    return wrapper


@decorator
def validate_typehints(__func__: Callable = None):
    """ Checks if arguments passed to wrapped functions, are instances of typehint classes
    If not raises Value error.
    Decorator does not change the return value, it's recommended if it's important to check correctness of given types.

    **!! Be aware that this may increase the function runtime. Not recommended for very simple functions. !!**

    Raises
    -------
    Value Error:
        Raises value error if passed arguments does not match the typehints.

    """
    @wraps(__func__)
    def wrapper(*args, **kwargs):
        all_arguments = dict(zip(inspect.getfullargspec(__func__).args, args))
        all_arguments.update(kwargs)
        for arg, anottation in __func__.__annotations__.items():
            if arg in all_arguments:
                if not isinstance(all_arguments[arg], anottation):
                    raise ValueError(f"""Expected <{anottation.__name__}> on argument "{arg}", got <{
                                     all_arguments[arg].__class__.__name__}> instead""")
        return __func__(*args, **kwargs)
    return wrapper
