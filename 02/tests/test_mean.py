import time
import pytest
from mean import mean


def test_mean_decorator(capsys):
    @mean(5)
    def slow_function():
        time.sleep(0.01)

    for _ in range(5):
        slow_function()

    captured = capsys.readouterr()
    output_lines = captured.out.strip().split("\n")

    assert len(output_lines) == 5  # Должно быть пять строк вывода
    for line in output_lines:
        # Проверяем, что каждая строка вывода содержит среднее время в секундах
        assert line.endswith(" sec")

    mean_time = float(output_lines[-1].split(" ")[0])
    assert abs(mean_time - 0.01) < 0.005  # Позволим погрешность в 5 миллисекунд


def test_mean_decorator_with_zero():
    # Должны получить исключение ValueError
    with pytest.raises(ValueError, match="Times must be grower than zero"):

        @mean(0)
        def foo():
            pass

        foo()


def test_mean_decorator_with_negative_times(capsys):
    # Должны получить исключение ValueError
    with pytest.raises(ValueError, match="Times must be grower than zero"):

        @mean(-1)
        def foo():
            pass

        foo()


def test_mean_decorator_with_small_times(capsys):
    @mean(2)
    def quick_function():
        time.sleep(0.005)

    for _ in range(100):
        quick_function()

    captured = capsys.readouterr()
    output_lines = captured.out.strip().split("\n")

    assert len(output_lines) == 100  # Должно быть три строки вывода
    for line in output_lines:
        # Проверяем, что каждая строка вывода содержит среднее время в секундах
        assert line.endswith(" sec")

    mean_time = float(output_lines[-1].split(" ")[0])
    assert abs(mean_time - 0.005) < 0.001  # Позволим погрешность в 1 миллисекунду


def test_mean_decorator_result():
    @mean(2)
    def add(a, b):
        return a + b

    for i in range(100):
        add(i, i)

    result = add(10, 2)
    assert result == 12
