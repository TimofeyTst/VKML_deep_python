import time
from mean import mean


def test_mean_decorator(capsys):
    @mean(30)
    def slow_function():
        time.sleep(0.01)

    slow_function()

    captured = capsys.readouterr()
    assert "0.01 sec" in captured.out


def test_mean_decorator_with_fast_function(capsys):
    @mean(500)
    def add_numbers(a, b):
        return a + b

    add_numbers(2, 3)

    captured = capsys.readouterr()
    # Нет задержки, так что время должно быть близким к 0
    assert "0.0 sec" in captured.out


def test_mean_decorator_with_large_number_of_iterations(capsys):
    @mean(1000)
    def slow_function():
        time.sleep(0.001)

    slow_function()

    captured = capsys.readouterr()
    assert "0.001 sec" in captured.out
