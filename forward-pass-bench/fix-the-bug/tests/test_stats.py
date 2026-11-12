import sys

sys.path.insert(0, "/app")
from stats import median


def test_odd_length():
    assert median([3, 1, 2]) == 2


def test_even_length():
    assert median([4, 1, 3, 2]) == 2.5


def test_already_sorted():
    assert median([1, 2, 3, 4, 5]) == 3


def test_input_not_modified():
    data = [3, 1, 2]
    median(data)
    assert data == [3, 1, 2]
