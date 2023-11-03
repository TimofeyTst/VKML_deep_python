import pytest
import asyncio
from async_client import Client

HOST = "localhost"
PORT = 8080


@pytest.mark.asyncio
async def test_client_task_count_mocked_worker(mocker):
    # Проверяем корректное формирование batched_url,
    # запуск нужного числа задач и вызов process url c нужными параметрами
    task_count = 3
    urls_file = "urls.txt"

    client = Client(HOST, PORT, task_count, urls_file, top_k=2, debug=True)

    # Создаем заглушку для aiohttp.ClientSession
    mocker.patch("aiohttp.ClientSession")

    mock_worker = mocker.AsyncMock(return_value="Mocked response")
    mock_que = mocker.AsyncMock(return_value="Mocked response")
    client.worker = mock_worker
    client.que = mock_que

    mock_get_url = mocker.Mock()
    urls = [f"url{i}" for i in range(task_count)]
    mock_get_url.return_value = urls
    client.get_url = mock_get_url

    await client.run_tasks()

    assert client.tasks_created == task_count
    assert mock_worker.call_count == task_count

    assert mock_get_url.call_count == 1
    assert mock_que.put.call_count == 4

    # Проверяем переданные параметры в queue
    got_calls = [mock_que.put.call_args_list[i].args[0] for i in range(task_count)]
    assert got_calls == urls

    # Проверяем, что после завершения run_tasks список пуст
    assert len(asyncio.all_tasks()) == 1


@pytest.mark.asyncio
async def test_client_file_len_lower_than_task_count(mocker):
    # Проверяем корректное формирование batched_url,
    # запуск нужного числа задач и вызов process url c нужными параметрами
    task_count = 15
    url_count = 5
    urls_file = "urls.txt"

    client = Client(HOST, PORT, task_count, urls_file, top_k=2, debug=True)

    # Создаем заглушку для aiohttp.ClientSession
    mocker.patch("aiohttp.ClientSession")

    mock_worker = mocker.AsyncMock(return_value="Mocked response")
    mock_que = mocker.AsyncMock(return_value="Mocked response")
    client.worker = mock_worker
    client.que = mock_que

    urls = [f"url{i}" for i in range(url_count)]
    mocker.patch("builtins.open", mocker.mock_open(read_data="\n".join(urls)))

    await client.run_tasks()

    assert client.tasks_created == task_count
    assert mock_worker.call_count == task_count

    assert mock_que.put.call_count == url_count + 1
    # Проверяем переданные параметры в process_url
    got_calls = [mock_que.put.call_args_list[i].args[0] for i in range(len(urls))]
    assert got_calls == urls

    # Проверяем, что после завершения run_tasks список пуст
    assert len(asyncio.all_tasks()) == 1


@pytest.mark.asyncio
async def test_client_file_len_grower_than_task_count(mocker):
    # Проверяем корректное формирование batched_url,
    # запуск нужного числа задач и вызов process url c нужными параметрами
    task_count = 5
    url_count = task_count * 3 + 2
    urls_file = "urls.txt"

    client = Client(HOST, PORT, task_count, urls_file, top_k=2, debug=True)

    # Создаем заглушку для aiohttp.ClientSession
    mocker.patch("aiohttp.ClientSession")

    mock_worker = mocker.AsyncMock(return_value="Mocked response")
    mock_que = mocker.AsyncMock(return_value="Mocked response")
    client.worker = mock_worker
    client.que = mock_que

    urls = [f"url{i}" for i in range(url_count)]
    mocker.patch("builtins.open", mocker.mock_open(read_data="\n".join(urls)))

    await client.run_tasks()

    assert client.tasks_created == task_count
    assert mock_worker.call_count == task_count

    assert mock_que.put.call_count == url_count + 1
    # Проверяем переданные параметры в process_url
    got_calls = [mock_que.put.call_args_list[i].args[0] for i in range(len(urls))]
    assert got_calls == urls

    # Проверяем, что после завершения run_tasks список пуст
    assert len(asyncio.all_tasks()) == 1


@pytest.mark.asyncio
async def test_client_file_len_equals_task_count(mocker):
    # Проверяем корректное формирование batched_url,
    # запуск нужного числа задач и вызов process url c нужными параметрами
    task_count = 5
    url_count = task_count
    urls_file = "urls.txt"

    client = Client(HOST, PORT, task_count, urls_file, top_k=2, debug=True)

    # Создаем заглушку для aiohttp.ClientSession
    mocker.patch("aiohttp.ClientSession")

    mock_worker = mocker.AsyncMock(return_value="Mocked response")
    mock_que = mocker.AsyncMock(return_value="Mocked response")
    client.worker = mock_worker
    client.que = mock_que

    urls = [f"url{i}" for i in range(url_count)]
    mocker.patch("builtins.open", mocker.mock_open(read_data="\n".join(urls)))

    await client.run_tasks()

    assert client.tasks_created == task_count
    assert mock_worker.call_count == task_count

    assert mock_que.put.call_count == url_count + 1
    # Проверяем переданные параметры в process_url
    got_calls = [mock_que.put.call_args_list[i].args[0] for i in range(len(urls))]
    assert got_calls == urls

    # Проверяем, что после завершения run_tasks список пуст
    assert len(asyncio.all_tasks()) == 1


@pytest.mark.asyncio
async def test_client_0_task_count():
    # Проверяем корректное формирование batched_url,
    # запуск нужного числа задач и вызов process url
    urls_file = "urls.txt"

    with pytest.raises(ValueError, match="Tasks count must be > 0"):
        Client(HOST, PORT, 0, urls_file, top_k=2, debug=True)

    with pytest.raises(ValueError, match="Tasks count must be > 0"):
        Client(HOST, PORT, -10, urls_file, top_k=2, debug=True)

    with pytest.raises(ValueError, match="Tasks count must be > 0"):
        Client(HOST, PORT, -150, urls_file, top_k=2, debug=True)


@pytest.mark.asyncio
async def test_client_fetch_and_parse_while_process(mocker):
    # Проверяем вызов нужного числа fetch_url & parse_html с нужными параметрами
    task_count = 7
    urls_file = "urls.txt"
    client = Client(HOST, PORT, task_count, urls_file, top_k=2, debug=True)

    # Создаем заглушку для aiohttp.ClientSession
    after_fetching = "Fetched request"
    mock_fetch = mocker.AsyncMock(return_value=after_fetching)
    mock_parse = mocker.Mock(return_value="Mocked response")
    client.fetch_url = mock_fetch
    client.parse_html = mock_parse

    urls = [f"url{i}" for i in range(task_count * 3 + 2)]
    mocker.patch("builtins.open", mocker.mock_open(read_data="\n".join(urls)))

    await client.run_tasks()

    assert client.tasks_created == task_count

    # Проверяем, что функции вызвались для каждого url с нужными параметрами
    assert mock_fetch.call_count == len(urls)
    got_urls_calls = [mock_fetch.call_args_list[i].args[1] for i in range(len(urls))]
    assert got_urls_calls == urls

    assert mock_parse.call_count == len(urls)
    got_parse_calls = [mock_parse.call_args_list[i].args[0] for i in range(len(urls))]
    expected_parse_calls = [after_fetching for _ in range(len(urls))]
    assert got_parse_calls == expected_parse_calls

    # Проверяем, что после завершения run_tasks список пуст
    assert len(asyncio.all_tasks()) == 1


@pytest.mark.asyncio
async def test_client_successfully_fetched_and_top_words_while_process(mocker):
    # Проверяем вызов нужного числа fetch_url & get_top_words с нужными параметрами
    task_count = 7
    urls_file = "urls.txt"
    client = Client(HOST, PORT, task_count, urls_file, top_k=2, debug=True)

    # Создаем заглушку для aiohttp.ClientSession
    after_fetching = "Fetched request"
    top_words = "Top words"
    mock_fetch = mocker.AsyncMock(return_value=after_fetching)
    mock_top_words = mocker.Mock(return_value=top_words)

    client.fetch_url = mock_fetch
    client.get_top_words = mock_top_words

    urls = [f"url{i}" for i in range(task_count * 3 + 2)]
    mocker.patch("builtins.open", mocker.mock_open(read_data="\n".join(urls)))

    await client.run_tasks()

    assert client.tasks_created == task_count

    # Проверяем, что функции вызвались для каждого url с нужными параметрами
    assert mock_fetch.call_count == len(urls)
    got_urls_calls = [mock_fetch.call_args_list[i].args[1] for i in range(len(urls))]
    assert got_urls_calls == urls

    assert mock_top_words.call_count == len(urls)
    got_top_words_calls = [
        mock_top_words.call_args_list[i].args[0] for i in range(len(urls))
    ]
    expected_top_words_calls = [after_fetching for _ in range(len(urls))]
    assert got_top_words_calls == expected_top_words_calls

    # Проверяем, что после завершения run_tasks список пуст
    assert len(asyncio.all_tasks()) == 1


@pytest.mark.asyncio
async def test_client_parse_html_empty(mocker):
    task_count = 7
    urls_file = "urls.txt"
    client = Client(HOST, PORT, task_count, urls_file, top_k=2, debug=True)

    top_words = "Top words"
    mock_top_words = mocker.Mock(return_value=top_words)
    client.get_top_words = mock_top_words

    result = client.parse_html("")
    assert result == top_words


@pytest.mark.asyncio
async def test_client_parse_html(mocker):
    task_count = 7
    urls_file = "urls.txt"
    client = Client(HOST, PORT, task_count, urls_file, top_k=2, debug=True)

    top_words = "Top words"
    mock_top_words = mocker.Mock(return_value=top_words)
    client.get_top_words = mock_top_words

    html_text = "<div id='content'><img src='image.jpg'></div>"
    result = client.parse_html(html_text)
    html_text2 = "<p>This is a test. Test text.</p>"
    result2 = client.parse_html(html_text2)

    assert result == top_words
    assert result2 == top_words


@pytest.mark.asyncio
async def test_client_get_top_words_empty_text(mocker):
    task_count = 7
    urls_file = "urls.txt"
    client = Client(HOST, PORT, task_count, urls_file, top_k=2, debug=True)

    text = ""
    result = client.get_top_words(text)
    assert result == {}


@pytest.mark.asyncio
async def test_client_get_top_words_no_words(mocker):
    task_count = 7
    urls_file = "urls.txt"
    client = Client(HOST, PORT, task_count, urls_file, top_k=2, debug=True)

    text = "!@#$%^&*()_+"
    result = client.get_top_words(text)
    assert result == {"!@#$%^&*()_+": 1}


@pytest.mark.asyncio
async def test_client_get_top_words_one_word(mocker):
    task_count = 7
    urls_file = "urls.txt"
    client = Client(HOST, PORT, task_count, urls_file, top_k=2, debug=True)

    text = "apple"
    result = client.get_top_words(text)
    assert result == {"apple": 1}


@pytest.mark.asyncio
async def test_client_get_top_words_repeated_words(mocker):
    task_count = 7
    urls_file = "urls.txt"
    client = Client(HOST, PORT, task_count, urls_file, top_k=2, debug=True)

    text = "apple banana apple cherry banana apple"
    result = client.get_top_words(text)
    assert result == {"apple": 3, "banana": 2}


@pytest.mark.asyncio
async def test_client_starting_run_tasks(mocker):
    # Тест на вызов run tasks в start
    task_count = 7
    urls_file = "urls.txt"
    client = Client(HOST, PORT, task_count, urls_file, top_k=2, debug=True)

    mock_run_task = mocker.Mock()
    client.run_tasks = mock_run_task
    mocker.patch("asyncio.get_event_loop")

    client.start()

    assert mock_run_task.call_count == 1
