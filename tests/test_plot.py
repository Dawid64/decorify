from decorify import plot_multiple, plot_single


def test_plot_multiple(monkeypatch):
    @plot_multiple
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


def test_plot_single(monkeypatch):
    @plot_single
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
