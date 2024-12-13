# Decorify 
[![PyPI - Downloads](https://img.shields.io/pypi/dm/decorify)](https://pypi.org/project/decorify/)
[![PyPI Latest Release](https://img.shields.io/pypi/v/decorify.svg)](https://pypi.org/project/decorify/)
![CI - Test](https://github.com/Dawid64/decorify/actions/workflows/python-app.yml/badge.svg)
[![GitHub Pages Documentation](https://img.shields.io/badge/GitHub_Pages-Documentation-blue)](https://dawid64.github.io/decorify/)

Python Library for decorators

Decorify  is a lightweight Python library without any dependencies that offers a collection of simple, reusable decorators to enhance your functions. These decorators cover common use cases like logging, timing, retrying, and more. 

## Installation
Install Decorators via pip:

```bash
pip install decorify 
```
## Table of Content
| Decorator | Main functionality |
| --- | --- |
| timeit | Measures the time of the function |
| timeout | Terminates the function after it runs for too long |
| mute | Disables stdout for duration of decorated function |
| validate_typehints | Ensures that typehints are followed, raising error if not |
| retry | If exception is raised function is retried up to predefined amount of times |
| rate_limiter | Limits number of function calls such that there are no function calls within set amount of seconds |
| time_limiter | Splits time into intervals, and limits the number of function calls within each interval |
| default_value | Set default value for function if exception is raised |
| grid_search | Allow user to perform grid search on each iteration of function call |
| redirect | Enables user to redirect function input / output |
| crawler | Looks for function calls structure and displays it as a tree or nested lists |

## Additional Modules
### Plotting (matplotlib)
- **plot_multiple**: Creates a plot of a function's return values
- **plot_single**: Creates a plot of a function's return 

# Contributing
Contributions are welcome! Please submit a pull request or open an issue to add new decorators or suggest improvements.

# License
This project is licensed under the Apache v2.0  License.

