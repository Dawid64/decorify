""" Module containing plotting functions """

from typing import Callable, Iterable, Any, Tuple, Dict, Literal
from functools import wraps
import matplotlib.pyplot as plt
from decorify.base import decorator


@decorator
def plot_multiple(plot_type: Literal["boxplot", "violin"] = "boxplot", __func__: Callable[[Any], Any] = None):
    """
    Decorator for creating a plot of a function's return values.

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

    @wraps(__func__)
    def inner_func(arguments: Iterable[Tuple[Iterable[Any], Dict[str, Any]]]):
        results = []
        for args, kwargs in arguments:
            results.append(__func__(*args, **kwargs))
        if plot_type == "violin":
            plt.violinplot(results)
        elif plot_type == "boxplot":
            plt.boxplot(results)
        else:
            raise ValueError("plot_type must be 'boxplot' or 'violin'")
        plt.show()
        return results

    return inner_func


def plot_single(plot_type: Literal["boxplot", "violin"] = "boxplot", __func__: Callable[[Any], Any] = None):
    """
    Decorator for creating a plot of a function's return values.

    Parameters
    ----------
    func : Callable
        Function to be decorated. It should return a list of values.

    Returns
    -------
    Callable
        Wrapped function that shows a plot of the original function's return values.
    """

    @wraps(__func__)
    def inner_func(*args, **kwargs):
        results = __func__(*args, **kwargs)
        if plot_type == "violin":
            plt.violinplot(results)
        elif plot_type == "boxplot":
            plt.boxplot(results)
        else:
            raise ValueError("plot_type must be 'boxplot' or 'violin'")
        plt.show()
        return results

    return inner_func
