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
    mocker_queue = mocker.Mock()
    client.url_queue = mocker_queue

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

    # Проверяем, что в очередь были добавлены все urls и None
    expected_args = [url for url in urls] + [None]
    assert mocker_queue.put.call_count == len(urls) + 1
    args = [mocker_queue.put.call_args_list[i].args[0] for i in range(len(urls) + 1)]
    assert args == expected_args


def test_client_many_thread_count(mocker):
    num_threads = 100
    urls_file = "urls.txt"
    debug = True

    # Создаем экземпляр Client
    client = Client(HOST, PORT, num_threads, urls_file, debug=debug)
    mocker_send_requests = mocker.Mock()
    client.send_requests = mocker_send_requests
    mocker_queue = mocker.Mock()
    client.url_queue = mocker_queue

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

    # Проверяем, что в очередь были добавлены все urls и None
    expected_args = [url for url in urls] + [None]
    assert mocker_queue.put.call_count == len(urls) + 1
    args = [mocker_queue.put.call_args_list[i].args[0] for i in range(len(urls) + 1)]
    assert args == expected_args


def test_client_correct_remain_urls(mocker):
    num_threads = 3
    urls_file = "urls.txt"
    debug = True

    # Создаем экземпляр Client
    client = Client(HOST, PORT, num_threads, urls_file, debug=debug)
    mocker_send_requests = mocker.Mock()
    client.send_requests = mocker_send_requests
    mocker_queue = mocker.Mock()
    client.url_queue = mocker_queue

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

    # Проверяем, что в очередь были добавлены все urls и None
    expected_args = [url for url in urls] + [None]
    assert mocker_queue.put.call_count == len(urls) + 1
    args = [mocker_queue.put.call_args_list[i].args[0] for i in range(len(urls) + 1)]
    assert args == expected_args


def test_client_1_thread(mocker):
    num_threads = 1
    urls_file = "urls.txt"
    debug = True

    # Создаем экземпляр Client
    client = Client(HOST, PORT, num_threads, urls_file, debug=debug)
    mocker_send_requests = mocker.Mock()
    client.send_requests = mocker_send_requests
    mocker_queue = mocker.Mock()
    client.url_queue = mocker_queue

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

    # Проверяем, что в очередь были добавлены все urls и None
    expected_args = [url for url in urls] + [None]
    assert mocker_queue.put.call_count == len(urls) + 1
    args = [mocker_queue.put.call_args_list[i].args[0] for i in range(len(urls) + 1)]
    assert args == expected_args


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
