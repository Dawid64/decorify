from pydecorators import (
    plot_decorator_single_output_function,
    plot_decorator_multiple_output_function,
)


def test_plot_decorator_single(monkeypatch):
    @plot_decorator_single_output_function
    def add(a: int, b: int):
        return a + b

    if_shown_graph = False

    def show():
        nonlocal if_shown_graph
        if_shown_graph = True

    monkeypatch.setattr("matplotlib.pyplot.show", show)
    results = add([((1, 2), {}), ((2, 3), {}), ((3, 4), {})])
    assert results == [3, 5, 7]
    assert if_shown_graph


def test_plot_decoratoror_multiple(monkeypatch):
    @plot_decorator_multiple_output_function
    def add(arguments):
        return [sum(x) for x in arguments]

    if_shown_graph = False

    def show():
        nonlocal if_shown_graph
        if_shown_graph = True

    monkeypatch.setattr("matplotlib.pyplot.show", show)
    results = add([[1, 5, 2], [4, 2, 1], [7, 8, 5]])
    assert results == [8, 7, 20]
    assert if_shown_graph
