from server import Server, Worker

HOST = "localhost"
PORT = 8080
DEBUG = True


def test_server_initialization():
    num_workers = 3
    top_k = 3
    # Создаем экземпляр сервера
    server = Server(HOST, PORT, num_workers, top_k, DEBUG)

    # Проверяем, что атрибуты инициализированы правильно
    assert server.host == HOST
    assert server.port == PORT
    assert server.num_workers == num_workers
    assert server.top_k == top_k
    assert server.debug == DEBUG

    # Проверяем, что другие атрибуты инициализированы согласно значению по умолчанию
    assert server.url_queue.empty()
    assert server.processed_urls == 0


def test_server_worker_threads_creation(mocker):
    num_workers = 3
    top_k = 3
    server = Server(HOST, PORT, num_workers, top_k, DEBUG)

    # Создаем моки для socket.socket и его методов
    start_listening_mock = mocker.Mock()
    server.start_listening = start_listening_mock
    start_worker = mocker.Mock()
    Worker.start = start_worker

    # Моки для threading.Thread
    mocker.patch("threading.Thread")

    # Запускаем метод start() на сервере
    server.start()

    # Проверяем, что было создано NUM_WORKERS потоков Worker
    assert len(server.workers) == num_workers
    assert start_worker.call_count == num_workers


def test_server_worker_process_url(mocker):
    # Создаем экземпляр Worker
    server = mocker.Mock()
    server.processed_urls = 0
    server.top_k = 2

    text_before_parsing = "This is a sample text for testing."
    text_after_parsing = "sample text after parsing."
    response = "response"

    worker = Worker(server)

    mock_parse_html = mocker.patch.object(worker, "parse_html")
    mock_parse_html.return_value = text_after_parsing

    mock_get_top_words = mocker.patch.object(worker, "get_top_words")
    mock_get_top_words.return_value = response

    worker.get_top_words.return_value = response
    worker.parse_html.return_value = text_after_parsing

    # Фиктивный URL
    url = "http://example.com"

    # Мокируем библиотеку requests
    mocker_requests = mocker.patch("requests.get")
    mocker_requests.return_value.status_code = 200
    mocker_requests.return_value.text = text_before_parsing

    # Вызываем метод process_url
    result = worker.process_url(url)

    # Проверяем, что библиотека requests была вызвана с правильными параметрами
    mocker_requests.assert_called_with(url, timeout=10)

    # Проверяем, что результат содержит ожидаемую информацию
    expected_result = f"Top 2 words in '{url[:20]}...': {response}"
    assert result == expected_result
    assert server.processed_urls == 1
    assert mock_parse_html.called_once_with(text_before_parsing)
    assert mock_get_top_words.called_once_with(text_after_parsing)


def test_server_worker_process_url_exception(mocker):
    # Создаем экземпляр Worker
    server = mocker.Mock()
    server.processed_urls = 0
    server.top_k = 2

    text_before_parsing = "This is a sample text for testing."
    text_after_parsing = "sample text after parsing."
    response = "response"

    worker = Worker(server)

    mock_parse_html = mocker.patch.object(worker, "parse_html")
    mock_parse_html.return_value = text_after_parsing

    mock_get_top_words = mocker.patch.object(worker, "get_top_words")
    mock_get_top_words.return_value = response

    worker.get_top_words.return_value = response
    worker.parse_html.return_value = text_after_parsing

    # Фиктивный URL
    url = "http://example.com"

    # Мокируем библиотеку requests
    mocker_requests = mocker.patch("requests.get")
    mocker_requests.return_value.status_code = 400
    mocker_requests.return_value.text = text_before_parsing

    # Вызываем метод process_url
    result = worker.process_url(url)

    # Проверяем, что библиотека requests была вызвана с правильными параметрами
    mocker_requests.assert_called_with(url, timeout=10)

    # Проверяем, что результат содержит ожидаемую информацию
    expected_result = '{"error": "Failed to retrieve the URL: http://example.com"}'
    assert result == expected_result
    assert server.processed_urls == 1
    assert mock_parse_html.called_once_with(text_before_parsing)
    assert mock_get_top_words.called_once_with(text_after_parsing)
