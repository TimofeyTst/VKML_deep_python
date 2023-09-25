from parse import parse_json
import json
import pytest


def test_parse_json(mocker):
    # Общий случай, когда все присутствует
    callback_mock = mocker.Mock()

    json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
    required_fields = ["key1"]
    keywords = ["word2"]

    parse_json(
        json_str,
        required_fields=required_fields,
        keywords=keywords,
        keyword_callback=callback_mock,
    )

    callback_mock.assert_called_once_with("word2")


def test_parse_json_required_fields_missing(mocker):
    # В json_str отсутствуют обязательные поля
    callback_mock = mocker.Mock()

    json_str = '{"key2": "Word1 word2", "key3": "word2 word3"}'
    required_fields = ["key1"]
    keywords = ["word2"]

    parse_json(
        json_str,
        required_fields=required_fields,
        keywords=keywords,
        keyword_callback=callback_mock,
    )

    # Проверяем, что callback не была вызвана
    callback_mock.assert_not_called()


def test_parse_json_keywords_missing(mocker):
    # Нет совпадающих ключевых слов
    callback_mock = mocker.Mock()

    json_str = '{"key1": "Word1 word2", "key2": "word3 word4"}'
    required_fields = ["key1", "key2"]
    keywords = ["word5"]

    parse_json(
        json_str,
        required_fields=required_fields,
        keywords=keywords,
        keyword_callback=callback_mock,
    )

    callback_mock.assert_not_called()  # Проверяем, что callback не была вызвана


def test_parse_json_multiple_keywords(mocker):
    # Несколько совпадающих ключевых слов
    callback_mock = mocker.Mock()

    json_str = '{"key1": "Word1 word2", "key2": "word2 word3 word4"}'
    required_fields = ["key1", "key2"]
    keywords = ["word2"]

    parse_json(
        json_str,
        required_fields=required_fields,
        keywords=keywords,
        keyword_callback=callback_mock,
    )

    # Проверяем, что callback была вызвана дважды
    callback_mock.assert_has_calls([mocker.call("word2"), mocker.call("word2")])


def test_parse_json_multiple_keywords_100_times(mocker):
    # Несколько совпадающих ключевых слов 100 раз
    callback_mock = mocker.Mock()

    data = {f"key{i}": "Word{i} word2" for i in range(100)}
    json_str = json.dumps(data)
    required_fields = [f"key{i}" for i in range(100)]
    keywords = ["word2"]

    parse_json(
        json_str,
        required_fields=required_fields,
        keywords=keywords,
        keyword_callback=callback_mock,
    )

    # Проверяем, что callback была вызвана 100 раз с ключевым словом "word2"
    expected_calls = [mocker.call("word2") for _ in range(100)]
    callback_mock.assert_has_calls(expected_calls)


def test_parse_json_no_callback(mocker):
    # Не передана функция callback
    json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
    required_fields = ["key1"]
    keywords = ["word2"]

    # Проверяем, что функция не вызывает ошибку при отсутствии callback
    parse_json(json_str, required_fields=required_fields, keywords=keywords)

    # Ничего не проверяем, так как нет callback


def test_parse_keywords_none():
    # keywords не переданы
    json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
    with pytest.raises(ValueError) as excinfo:
        parse_json(json_str, required_fields=["key1"])
    assert "required_fields and keywords cannot be empty" in str(excinfo.value)


def test_parse_keywords_empty():
    # keywords пустой
    json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
    with pytest.raises(ValueError) as excinfo:
        parse_json(json_str, required_fields=["key1"], keywords=[])
    assert "required_fields and keywords cannot be empty" in str(excinfo.value)


def test_parse_required_fields_none():
    # keywords не переданы
    json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
    with pytest.raises(ValueError) as excinfo:
        parse_json(json_str, keywords=["key1"])
    assert "required_fields and keywords cannot be empty" in str(excinfo.value)


def test_parse_required_fields_empty():
    # keywords пустой
    json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
    with pytest.raises(ValueError) as excinfo:
        parse_json(json_str, required_fields=[], keywords=["key1"])
    assert "required_fields and keywords cannot be empty" in str(excinfo.value)


def test_parse_all_params_none():
    # keywords & required_fields не переданы
    json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
    with pytest.raises(ValueError) as excinfo:
        parse_json(json_str)
    assert "required_fields and keywords cannot be empty" in str(excinfo.value)


def test_parse_all_params_empty():
    # keywords & required_fields пусты
    json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
    with pytest.raises(ValueError) as excinfo:
        parse_json(json_str, required_fields=[], keywords=[])
    assert "required_fields and keywords cannot be empty" in str(excinfo.value)


def test_parse_json_empty_input():
    # Входная строка пуста
    with pytest.raises(ValueError) as excinfo:
        parse_json("", required_fields=["key1"], keywords=["word2"])
    assert "json_str cannot be empty" in str(excinfo.value)


def test_parse_json_invalid_json():
    # Передается некорректный JSON
    with pytest.raises(json.JSONDecodeError):
        parse_json("invalid_json", required_fields=["key1"], keywords=["word2"])
