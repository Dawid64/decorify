from pydecorators import exception_handling_default_value


def test_exception_handler_structure():
    @exception_handling_default_value
    def div_zero(a, b):
        return a / b

    @exception_handling_default_value(100)
    def div_hundred(a, b):
        return a / b

    assert div_zero(1, 0) == 0
    assert div_hundred(50, 0) == 100

