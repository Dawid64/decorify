from decorify import decorator
from functools import wraps


def test_base_structure():
    @decorator
    def test_decorator(value=2, __func__=None):
        @wraps(__func__)
        def wrapped(*args, **kwargs):
            return __func__(*args, **kwargs) * value
        return wrapped

    @test_decorator
    def add_double(a, b):
        return a + b

    @test_decorator(3)
    def add_triple(a, b):
        return a + b

    assert add_double(1, 2) == 6
    assert add_triple(1, 2) == 9
