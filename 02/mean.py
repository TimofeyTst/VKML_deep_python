import time


def mean(times: int):
    if times <= 0:
        raise ValueError("Times must be grower than zero")

    total_times = []

    def time_exec(func):
        def wrapper(*args, **kwargs):
            nonlocal total_times
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()

            total_times.append(end - start)
            if len(total_times) > times:
                total_times.pop(0)  # Удалить из начала

            mean_time = sum(total_times) / len(total_times)
            print(f"{mean_time} sec")
            return result

        return wrapper

    return time_exec
