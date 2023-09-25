import time


def mean(times: int):
    def time_exec(func):
        def wrapper(*args, **kwargs):
            total_time = 0

            for _ in range(times):
                start = time.time()
                func(*args, **kwargs)
                end = time.time()
                total_time += end - start

            mean_time = round(total_time / times, 3)
            print(f"{mean_time} sec")

        return wrapper

    return time_exec
