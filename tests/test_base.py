from pydecorators import decorator
from functools import wraps


def test_base_structure():
    @decorator
    def test_decorator(func: int, value=2):
        @wraps(func)
        def wrapped(*args, **kwargs):
            return func(*args, **kwargs) * value
        return wrapped

    @test_decorator
    def add_double(a, b):
        return a + b

    @test_decorator(3)
    def add_triple(a, b):
        return a + b

    assert add_double(1, 2) == 6
    assert add_triple(1, 2) == 9
