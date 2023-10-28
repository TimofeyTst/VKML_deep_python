import pytest
from client import Client

HOST = "localhost"
PORT = 8080


def test_client_initialization():
    num_threads = 10
    urls_file = "urls.txt"
    debug = True

    client = Client(HOST, PORT, num_threads, urls_file, debug=debug)

    assert client.host == HOST
    assert client.port == PORT
    assert client.num_threads == num_threads
    assert client.urls_file == urls_file
    assert client.debug == debug


def test_client_thread_count(mocker):
    num_threads = 3
    urls_file = "urls.txt"
    debug = True

    # Создаем экземпляр Client
    client = Client(HOST, PORT, num_threads, urls_file, debug=debug)
    mocker_send_requests = mocker.Mock()
    client.send_requests = mocker_send_requests

    # Создаем мок для открытия файла и возвращаем список URL'ов
    urls = ["url1", "url2", "url3"]
    mocker.patch("builtins.open", mocker.mock_open(read_data="\n".join(urls)))

    # Создаем моки для потоков
    mocker_thread = mocker.patch("threading.Thread")

    # Вызываем метод start() на клиенте
    client.start()

    # Проверяем, что создано нужное количество потоков
    assert mocker_thread.call_count == num_threads
    thread = mocker_thread.return_value
    assert thread.start.call_count == num_threads
    assert thread.join.call_count == num_threads

    # Проверяем, что каждый поток создан с правильными аргументами
    expected_args = [[url] for url in urls]

    for i in range(num_threads):
        target = mocker_thread.call_args_list[i][1]["target"]
        args = mocker_thread.call_args_list[i][1]["args"][0]
        assert target == mocker_send_requests
        assert args == expected_args[i]


def test_client_many_thread_count(mocker):
    num_threads = 100
    urls_file = "urls.txt"
    debug = True

    # Создаем экземпляр Client
    client = Client(HOST, PORT, num_threads, urls_file, debug=debug)
    mocker_send_requests = mocker.Mock()
    client.send_requests = mocker_send_requests

    # Создаем мок для открытия файла и возвращаем список URL'ов
    urls = ["url1", "url2", "url3"]
    mocker.patch("builtins.open", mocker.mock_open(read_data="\n".join(urls)))

    # Создаем моки для потоков
    mocker_thread = mocker.patch("threading.Thread")

    # Вызываем метод start() на клиенте
    client.start()

    # Проверяем, что создано нужное количество потоков
    assert mocker_thread.call_count == num_threads
    thread = mocker_thread.return_value
    assert thread.start.call_count == num_threads
    assert thread.join.call_count == num_threads

    # Проверяем, что каждый поток создан с правильными аргументами
    expected_args = [[url] for url in urls]
    expected_args.extend([[] for _ in range(num_threads - len(urls))])

    thread_args = []
    for i in range(num_threads):
        target = mocker_thread.call_args_list[i][1]["target"]
        thread_args.append(mocker_thread.call_args_list[i][1]["args"][0])
        assert target == mocker_send_requests

    assert thread_args == expected_args


def test_client_correct_remain_urls(mocker):
    num_threads = 3
    urls_file = "urls.txt"
    debug = True

    # Создаем экземпляр Client
    client = Client(HOST, PORT, num_threads, urls_file, debug=debug)
    mocker_send_requests = mocker.Mock()
    client.send_requests = mocker_send_requests

    # Создаем мок для открытия файла и возвращаем список URL'ов
    urls = [
        "url1",
        "url2",
        "url3",
        "url4",
        "url5",
        "url6",
        "url7",
        "url8",
        "url9",
        "url10",
        "url11",
    ]
    mocker.patch("builtins.open", mocker.mock_open(read_data="\n".join(urls)))

    # Создаем моки для потоков
    mocker_thread = mocker.patch("threading.Thread")

    # Вызываем метод start() на клиенте
    client.start()

    # Проверяем, что создано нужное количество потоков
    assert mocker_thread.call_count == num_threads
    thread = mocker_thread.return_value
    assert thread.start.call_count == num_threads
    assert thread.join.call_count == num_threads

    # Проверяем, что каждый поток создан с правильными аргументами
    expected_args = [
        ["url1", "url2", "url3", "url4"],
        ["url5", "url6", "url7", "url8"],
        ["url9", "url10", "url11"],
    ]

    thread_args = []
    for i in range(num_threads):
        target = mocker_thread.call_args_list[i][1]["target"]
        thread_args.append(mocker_thread.call_args_list[i][1]["args"][0])
        assert target == mocker_send_requests

    assert thread_args == expected_args


def test_client_1_thread(mocker):
    num_threads = 1
    urls_file = "urls.txt"
    debug = True

    # Создаем экземпляр Client
    client = Client(HOST, PORT, num_threads, urls_file, debug=debug)
    mocker_send_requests = mocker.Mock()
    client.send_requests = mocker_send_requests

    # Создаем мок для открытия файла и возвращаем список URL'ов
    urls = ["url1", "url2", "url3"]
    mocker.patch("builtins.open", mocker.mock_open(read_data="\n".join(urls)))

    # Создаем моки для потоков
    mocker_thread = mocker.patch("threading.Thread")

    # Вызываем метод start() на клиенте
    client.start()

    # Проверяем, что создано нужное количество потоков
    assert mocker_thread.call_count == num_threads
    thread = mocker_thread.return_value
    assert thread.start.call_count == num_threads
    assert thread.join.call_count == num_threads

    # Проверяем, что каждый поток создан с правильными аргументами
    target = mocker_thread.call_args_list[0][1]["target"]
    thread_args = mocker_thread.call_args_list[0][1]["args"][0]
    assert target == mocker_send_requests
    assert thread_args == urls


def test_send_requests_lower_0_thread(mocker):
    urls_file = "urls.txt"
    debug = True

    # Создаем экземпляр Client
    with pytest.raises(ValueError, match="Threads count must be > 0"):
        Client(HOST, PORT, 0, urls_file, debug=debug)

    with pytest.raises(ValueError, match="Threads count must be > 0"):
        Client(HOST, PORT, -10, urls_file, debug=debug)

    with pytest.raises(ValueError, match="Threads count must be > 0"):
        Client(HOST, PORT, -150, urls_file, debug=debug)
