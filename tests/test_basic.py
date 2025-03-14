from pytest import raises
from decorify.basic import timeit, grid_search, timeout, rate_limiter, interval_rate_limiter
from time import sleep, perf_counter


def test_timeit():

    @timeit
    def sleep_function(sleep_time):
        sleep(sleep_time)
        return 2

    sleep_time = 0.4
    function_result, function_time = sleep_function(sleep_time)
    assert function_result == 2
    assert abs(function_time - sleep_time) <= 1e-2


def test_timeit_accuracy():

    @timeit(1)
    def sleep_function(sleep_time):
        sleep(sleep_time)
        return 2

    sleep_time = 0.41
    function_result, function_time = sleep_function(sleep_time)
    assert function_result == 2
    assert function_time == 0.4


def test_grid_search():

    @grid_search(argument_parameters={'a': [1, 2], 'b': [2, 3]})
    def add(a=1, b=1):
        return a + b

    best_args, best_value = add()
    assert best_args == (2, 3)
    assert best_value == 5


def test_grid_search_all_values():

    @grid_search(argument_parameters={'a': [1, 2], 'b': [2, 3]}, return_all_values=True)
    def add(a=1, b=1):
        return a + b

    all_values = add()
    assert isinstance(all_values, dict)
    assert (1, 2) in all_values


def test_grid_search_without_arguments():

    @grid_search(argument_parameters={'a': [1, 2], 'b': [2, 3]}, return_without_arguments=True)
    def add(a=1, b=1, c=3):
        return (a + b) * c

    value = add(c=2)
    assert value == 10


def test_timeout():
    @timeout(0.1)
    def foo(val):
        sleep(val)
        return val

    assert foo(0.05) == 0.05


def test_timeout_raise():
    @timeout(0.05)
    def foo(val):
        sleep(val)
        return val

    with raises(TimeoutError):
        foo(0.1)


def test_timeout_default():
    @timeout(0.1, None)
    def foo(val):
        sleep(val)
        return val

    assert foo(0.15) is None


def test_timeout_while():
    @timeout(0.1, None)
    def foo():
        value = 1
        while True:
            value += 1
        return value

    assert foo() is None


def test_timeout_error():
    @timeout(0.1, None)
    def foo():
        raise ValueError()

    with raises(ValueError):
        foo()


def test_rate_limiter_non_activated():
    @rate_limiter(0.05, 2)
    def foo(val):
        return val
    start_time = perf_counter()
    val = foo(1)
    assert perf_counter() - start_time < 0.05
    assert val == 1


def test_rate_limiter_activated():
    @rate_limiter(0.05, 1)
    def foo(val):
        return val
    start_time = perf_counter()
    val1 = foo(1)
    assert perf_counter() - start_time < 0.05
    val2 = foo(2)
    assert perf_counter() - start_time > 0.05
    assert perf_counter() - start_time < 0.1
    assert val1 == 1
    assert val2 == 2


def test_rate_limiter_many():
    @rate_limiter(0.05, 5)
    def foo():
        return
    start_time = perf_counter()
    for i in range(11):
        foo()
    assert perf_counter() - start_time > 0.1
    assert perf_counter() - start_time < 0.2


def test_time_limiter_non_activated():
    @interval_rate_limiter(0.05, 2)
    def foo(val):
        return val
    start_time = perf_counter()
    val = foo(1)
    assert perf_counter() - start_time < 0.05
    assert val == 1


def test_time_limiter_activated():
    start_time = perf_counter()

    @interval_rate_limiter(0.05, 1)
    def foo(val):
        return val
    val1 = foo(1)
    assert perf_counter() - start_time < 0.05
    val2 = foo(2)
    assert perf_counter() - start_time > 0.05
    assert perf_counter() - start_time < 0.1
    assert val1 == 1
    assert val2 == 2


def test_time_limiter_many():
    @interval_rate_limiter(0.1, 5)
    def foo():
        return
    start_time = perf_counter()
    sleep(0.05)
    for _ in range(10):
        foo()
    assert perf_counter() - start_time > 0.1
    assert perf_counter() - start_time < 0.15


def test_time_sync():
    time_limit = 0.2

    @timeit(1)
    @interval_rate_limiter(time_limit, 1, sync_with_clock=True)
    @timeit(1)
    def foo():
        return
    start_time = perf_counter()
    (_, inner_time1), foo_time1 = foo()
    (_, inner_time2), foo_time2 = foo()
    (_, inner_time3), foo_time3 = foo()
    assert perf_counter() - start_time < time_limit * 3
    assert foo_time2 >= foo_time1
    assert time_limit >= foo_time2
    assert foo_time3 >= time_limit
    assert foo_time3 >= foo_time1 + time_limit
    assert inner_time1 == foo_time1
    assert inner_time2 <= foo_time2
    assert inner_time3 == foo_time3 - time_limit
