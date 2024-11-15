Decorify
=============
.. automodule:: decorify
   :noindex:
   :members:
   :exclude-members: default_value, grid_search, timeout, timeit, validate_typehints

Functions
---------

.. autosummary::
   :nosignatures:
   
   timeit
   grid_search
   timeout
   default_value
   validate_typehints

Submodules
----------

.. toctree::
   :maxdepth: 2

   /decorify/plot/index

Package Contents
----------------

.. py:function:: timeit(accuracy: int = 2)

   Decorator for measuring execution time of a function.

   :param accuracy: Rounding place of the value.
   :type accuracy: int

   :returns: Wrapped function that returns a tuple of original function's result and
             measured execution time.
   :rtype: function


.. py:function:: grid_search(argument_parameters: Dict[str, list], return_all_values: bool = False, key=max, return_without_arguments: bool = False)

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


.. py:function:: timeout(time: float, default_value: Any = mp_TimeoutError)

   Decorated function is run in new process while still sharing memory, if the time limit is reached
   function returns default value or raises TimeoutError if default_value is not set.

   :param time: The maximum allowed time for the function to execute, in seconds.
   :type time: float
   :param default_value: Default output value if timeout is reached. If value not changed, decorator raises TimeoutError.
   :type time: Any

   :raises TimeoutError:: Raises TimeoutError if default_value argument is TimeoutError and specified time is reached.

   :returns: Functions output if function reached in time limit or default value if such value was set, and time limit was reached.
   :rtype: function


.. py:function:: default_value(default_value: Any = None, *, logger: Optional[logging.Logger] = None)

   Decorator for assigning default value if function fails

   :param default_value: Default value which is set if the funciton fails
   :type default_value: Any
   :param logger: Logger for logging warning if the function failed and the default value was returned
   :type logger: logging.Logger

   :returns: Wrapped function that returns defealut value if exception is raised
   :rtype: function


.. py:function:: validate_typehints()

   Checks if arguments passed to wrapped functions, are instances of typehint classes
   If not raises Value error.
   Decorator does not change the return value, it's recommended if it's important to check correctness of given types.

   **!! Be aware that this may increase the function runtime. Not recommended for very simple functions. !!**

   :raises Value Error:: Raises value error if passed arguments does not match the typehints.

