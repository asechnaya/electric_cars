import statistics


def test_maximum_is_ok():
    maximum = round(max([100, 100.211]), 2)
    assert maximum == 100.21


def test_minimum_is_ok():
    minimum = round(min([0.917, 9]), 2)
    assert minimum == 0.92


def test_mean_is_ok():
    mean = round(statistics.mean([1, 2, 11.2, 123]), 2)
    assert mean == 34.3
