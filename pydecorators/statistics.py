from typing import Iterable, Any, Tuple, Dict, Literal
from functools import wraps
import matplotlib.pyplot as plt
from .base import decorator


@decorator
def plot_decorator_single_output_function(func, plot_type: Literal["boxplot", "violin"] = "boxplot"):
    """
    Decorator for creating plots of a function's return values.

    Parameters
    ----------
    func : Callable
        Function to be decorated. It should return a single value.

    Returns
    -------
    Callable
        Wrapped function that shows a plot of the original function's return values.
        And takes a list of tuples as input, where each tuple contains the arguments and keyword arguments for the original function.
    """

    @wraps(func)
    def inner_func(arguments: Iterable[Tuple[Iterable[Any], Dict[str, Any]]]):
        results = []
        for args, kwargs in arguments:
            results.append(func(*args, **kwargs))
        if plot_type == "violin":
            plt.violinplot(results)
        elif plot_type == "boxplot":
            plt.boxplot(results)
        else:
            raise ValueError("plot_type must be 'boxplot' or 'violin'")
        plt.show()
        return results

    return inner_func


def plot_decorator_multiple_output_function(func, plot_type: Literal["boxplot", "violin"] = "boxplot"):
    """
    Decorator for creating plots of a function's return values.

    Parameters
    ----------
    func : Callable
        Function to be decorated. It should return a list of values.

    Returns
    -------
    Callable
        Wrapped function that shows a plot of the original function's return values.
    """

    @wraps(func)
    def inner_func(*args, **kwargs):
        results = func(*args, **kwargs)
        if plot_type == "violin":
            plt.violinplot(results)
        elif plot_type == "boxplot":
            plt.boxplot(results)
        else:
            raise ValueError("plot_type must be 'boxplot' or 'violin'")
        plt.show()
        return results

    return inner_func
