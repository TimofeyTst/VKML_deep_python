import cProfile
import pstats
from io import StringIO


class ProfiledFunction:
    def __init__(self, func):
        self.func = func
        self.profiler = cProfile.Profile()

    def __call__(self, *args, **kwargs):
        self.profiler.enable()
        result = self.func(*args, **kwargs)
        self.profiler.disable()
        return result

    def print_stat(self):
        stats = StringIO()
        sortby = "calls"
        ps = pstats.Stats(self.profiler, stream=stats).sort_stats(sortby)
        ps.print_stats()
        print(f"================ {self.func.__name__} stat =================")
        print(stats.getvalue())


def profile(func):
    return ProfiledFunction(func)


def main():
    @profile
    def my_function():
        for i in range(1000000):
            _ = i * 2

    @profile
    def add(a, b):
        return a + b

    @profile
    def sub(a, b):
        return a - b

    my_function()
    my_function()
    my_function()

    my_function.print_stat()
    add(1, 2)
    add(4, 5)
    sub(4, 5)
    add.print_stat()
    sub.print_stat()


if __name__ == "__main__":
    main()
