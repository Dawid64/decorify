decorify.plot
=============

.. py:module:: decorify.plot


Module containing plotting functions



Functions
---------

.. autosummary::

   plot_multiple
   plot_single


Module Contents
---------------

.. py:function:: plot_multiple(plot_type: Literal['boxplot', 'violin'] = 'boxplot', __func__: Callable[[Any], Any] = None)

   Decorator for creating a plot of a function's return values.

   :param func: Function to be decorated. It should return a single value.
   :type func: Callable

   :returns: Wrapped function that shows a plot of the original function's return values.
             And takes a list of tuples as input, where each tuple contains the arguments and keyword arguments for the original function.
   :rtype: Callable


.. py:function:: plot_single(plot_type: Literal['boxplot', 'violin'] = 'boxplot', __func__: Callable[[Any], Any] = None)

   Decorator for creating a plot of a function's return values.

   :param func: Function to be decorated. It should return a list of values.
   :type func: Callable

   :returns: Wrapped function that shows a plot of the original function's return values.
   :rtype: Callable


