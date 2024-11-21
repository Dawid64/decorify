from decorify.profiling import crawler, Tree, generate_ascii_tree


def test_profiling_stack():
    def func_a():
        return sum([1, 1])

    @crawler(as_list=True)
    def func_b():
        return func_a() + func_a()

    assert func_b() == ['func_b', ['func_a'], ['func_a']]


def test_profiling_stack_build_ins():
    def func_a():
        return sum([1, 1])

    @crawler(build_ins=True, as_list=True)
    def func_b():
        return func_a() + func_a()

    assert func_b() == ['func_b', ['func_a', ['sum']], ['func_a', ['sum']]]


def test_profiling_tree():
    def func_a():
        return sum([1, 1])

    @crawler(as_tree=True)
    def func_b():
        return func_a() + func_a()

    assert isinstance(func_b(), Tree)


def test_ascii_generator():
    sample = ['add_1', ['add_2', ['add_2', ['add_2', ['add_2', ['add_2'], ['add_2']], ['add_2']], [
        'add_2', ['add_2'], ['add_2']]], ['add_2', ['add_2', ['add_2'], ['add_2']], ['add_2']]]]
    ascii_tree = generate_ascii_tree(sample)
    assert isinstance(ascii_tree, str)
