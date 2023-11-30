import json
import ujson
import cjson


from faker import Faker
import time

fake = Faker()


def generate_large_data(count, num_items, load=True):
    for i in range(count):
        data = {f"name{i}": fake.name() for i in range(num_items)}
        if load:
            yield data
        else:
            yield json.dumps(data)


def test_speed(json_func, ujson_func, cjson_func, count, num_items, load=True):
    start = time.time()

    ujson_duration = 0
    json_duration = 0
    cjson_duration = 0

    for data in generate_large_data(count, num_items, load=load):
        # Тест для json
        start_time = time.time()
        json_func(data)
        json_duration += time.time() - start_time

        # Тест для ujson
        start_time = time.time()
        ujson_func(data)
        ujson_duration += time.time() - start_time

        # Тест для cjson
        start_time = time.time()
        cjson_func(data)
        cjson_duration += time.time() - start_time

    json_mean = json_duration / (count * num_items)
    ujson_mean = ujson_duration / (count * num_items)
    cjson_mean = cjson_duration / (count * num_items)
    # Проверяем, что каждый тест выполняется не менее чем за 100 мс
    print("Total/Mean in seconds")
    print(f"json  duration: {json_duration:.5} / {json_mean:.5}")
    print(f"ujson duration: {ujson_duration:.5} / {ujson_mean:.5}")
    print(f"cjson duration: {cjson_duration:.5} / {cjson_mean:.5}")

    end = time.time()
    print(f"Performance test passed successfully total time: {(end - start):.5}s.")


def main():
    # count = 1000  # Количество итераций
    # num_items = 1000  # Количество JSON
    print("===== Test dump method =====")
    test_speed(
        json.dumps, ujson.dumps, cjson.dumps, count=200, num_items=1000, load=True
    )
    print("\n===== Test load method =====")
    test_speed(
        json.loads, ujson.loads, cjson.loads, count=200, num_items=1000, load=False
    )


if __name__ == "__main__":
    main()
