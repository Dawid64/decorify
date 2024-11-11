# Decorify 
Python Library for decorators


Decorify  is a lightweight Python library without any dependencies that offers a collection of simple, reusable decorators to enhance your functions. These decorators cover common use cases like logging, timing, retrying, and more. 

## Installation
Install Decorators via pip:

```bash
pip install decorify 
```
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

