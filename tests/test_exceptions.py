import logging
from decorify import default_value, validate_typehints
from pytest import raises


def test_exception_handler_default():
    @default_value
    def div_zero(a, b):
        return a / b
    assert div_zero(1, 0) == None


def test_exception_handler_default_set():
    @default_value(100)
    def div_hundred(a, b):
        return a / b
    assert div_hundred(50, 0) == 100


def test_exception_handler_default_logger(caplog):
    caplog.set_level(logging.WARNING)
    logger = logging.getLogger('Logger testowy')

    @default_value(100, logger=logger)
    def div_hundred(a, b):
        return a / b
    assert div_hundred(50, 0) == 100

    assert "Set default value in function 'div_hundred', because of 'division by zero'" in caplog.text


def test_validate_typehints():
    @validate_typehints
    def add(a: float, b: int):
        return a + b

    assert add(2.0, 2) == 4
    assert add(a=2.0, b=2) == 4
    assert add(b=2, a=2.0) == 4

    with raises(ValueError):
        add(2.0, 2.0)

    with raises(ValueError):
        add(2.0, b="")
