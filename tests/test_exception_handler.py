from pydecorators import exception_handling_default_value
import logging

def test_exception_handler_default():
    @exception_handling_default_value
    def div_zero(a, b):
        return a / b
    assert div_zero(1, 0) == None





def test_exception_handler_default_set():
    @exception_handling_default_value(100)
    def div_hundred(a, b):
        return a / b
    assert div_hundred(50, 0) == 100



def test_exception_handler_default_logger(caplog):
    caplog.set_level(logging.WARNING)
    logger = logging.getLogger('Logger testowy')

    @exception_handling_default_value(100 , logger=logger)
    def div_hundred(a, b):
        return a / b
    assert div_hundred(50, 0) == 100

    assert "Set default value in function 'div_hundred', because of 'division by zero'" in caplog.text


def test_expception_hander_typehint():
    @test_expception_hander_typehint
    def bt(a,b):



