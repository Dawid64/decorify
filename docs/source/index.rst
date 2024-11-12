Decorify
=============

.. py:module:: decorify

# Decorify
Python Library for decorators


Decorify  is a lightweight Python library without any dependencies that offers a collection of simple, reusable decorators to enhance your functions. These decorators cover common use cases like logging, timing, retrying, and more.


Functions
---------

.. autosummary::

   decorator
   timeit
   grid_search
   time_restriction
   default_value
   validate_typehints

Submodules
----------

.. toctree::
   :maxdepth: 2

   /decorify/plot/index

Package Contents
----------------

.. py:function:: decorator(dec: Callable)

.. py:function:: timeit(accuracy: int = 2, __func__: Callable[[Any], Any] = None) -> Callable[[Any], Any]

   Decorator for measuring execution time of a function.

   :param accuracy: Rounding place of the value.
   :type accuracy: int

   :returns: Wrapped function that returns a tuple of original function's result and
             measured execution time.
   :rtype: function


.. py:function:: grid_search(argument_parameters: Dict[str, list], return_all_values: bool = False, key=max, return_without_arguments: bool = False, __func__: Callable[[Any], Any] = None) -> Callable[[Any], Any]

   Perfomes the grid search on passed arguments.
   The function can either return found arguments and it's value,
   only value or dictionary of all search aruments and it's values.

   :param argument_parameters: Rounding place of the value.
   :type argument_parameters: int
   :param return_all_values: If True wrapped function returns dictionary {Parameters:value}
   :type return_all_values: bool
   :param key: Performes following function to find specific value
   :type key: Callable, default=max
   :param return_without_arguments: Returns only found value
   :type return_without_arguments: bool

   :returns: Wrapped function that returns a tuple of found arguments and
             their value for function.
   :rtype: function


.. py:function:: time_restriction(time: float, __func__: Callable[[Any], Any] = None) -> Callable[[Any], Any]

   A decorator that restricts the execution time of a function. If the function does not complete
   within the specified time limit, it is terminated and a TimeoutError is raised.

   :param func: The function to be decorated.
   :type func: Callable[[Any], Any]
   :param time: The maximum allowed time for the function to execute, in seconds.
   :type time: float

   :returns: The wrapped function with time restriction applied.
   :rtype: Callable[[Any], Any]


.. py:function:: default_value(default_value: Any = None, *, logger: Optional[logging.Logger] = None, __func__: Callable = None)

   Decorator for assigning default value if function fails

   :param default_value: Default value which is set if the funciton fails
   :type default_value: Any
   :param logger: Logger for logging warning if the function failed and the default value was returned
   :type logger: logging.Logger

   :returns: Wrapped function that returns defealut value if exception is raised
   :rtype: function


.. py:function:: validate_typehints(__func__: Callable = None)

   Checks if arguments passed to wrapped functions, are instances of typehint classes
   If not raises Value error.
   Decorator does not change the return value, it's recommended if it's important to check correctness of given types.

   **!! Be aware that this may increase the function runtime. Not recommended for very simple functions. !!**

   :raises Value Error:: Raises value error if passed arguments does not match the typehints.



.. [#f1] Created with `sphinx-autoapi <https://github.com/readthedocs/sphinx-autoapi>`_