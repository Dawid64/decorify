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

## Table of content

| function | description |
| --- | --- |
| **timeit** | Measures the execution time of a function |
| **validate_typehints** | Raises exception if argument doesn't match the typehint |
| **timeout** | Function either raises error or returns default value if time limit is reached |
| **retry** | Retries a function again up to *n* times if fails
| **default_value** | Sets default value for function if error occurs
| **and more ...** | More functions and more precise description can be found in libraries documentation


## Features

### Basic
- **timeit**: Measures the execution time of a function
- **grid_search**: Preforms a grid search on passed arguments

### Iterative
- **retry**: Automatically retries a function if it raises an exception, with specified numer of maximal tries
- **loop**: Runs the function n times and returns list of values
- **average**: Automaticly calulates avrerage from n runs of a function

### Exceptions
- **default_value**: Assigns a default value to the function
- **validate_typehints**: Checks if all the typehits passed to the function are of correct type

### Plotting (matplotlib)
- **plot_multiple**: Creates a plot of a function's return values
- **plot_single**: Creates a plot of a function's return 

# Contributing
Contributions are welcome! Please submit a pull request or open an issue to add new decorators or suggest improvements.

# License
This project is licensed under the Apache v2.0  License.

