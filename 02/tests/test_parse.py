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

    callback_mock.assert_called_once_with("key1", "word2")


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
    expected_calls = [mocker.call("key1", "word2"), mocker.call("key2", "word2")]
    assert callback_mock.call_args_list == expected_calls


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
    expected_calls = [mocker.call(required_fields[i], "word2") for i in range(100)]
    assert callback_mock.call_args_list == expected_calls


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


def test_parse_json_keywords_case_insensetive_keywords(mocker):
    # Регистронезависимый вызов callback
    callback_mock = mocker.Mock()

    json_str = '{"key1": "Word1 wOrd2", "key2": "word3 word4"}'
    required_fields = ["key1", "key2"]
    keywords = ["woRD2"]

    parse_json(
        json_str,
        required_fields=required_fields,
        keywords=keywords,
        keyword_callback=callback_mock,
    )

    callback_mock.assert_called_once_with("key1", "wOrd2")


def test_parse_json_multiple_case_insensetive_keyword_100_times(mocker):
    # Несколько совпадающих ключевых слов 100 раз с разным регистром
    callback_mock = mocker.Mock()

    data = {f"key{i}": "Word{i} WORd2" for i in range(100)}
    json_str = json.dumps(data)
    required_fields = [f"key{i}" for i in range(100)]
    keywords = ["worD2"]

    parse_json(
        json_str,
        required_fields=required_fields,
        keywords=keywords,
        keyword_callback=callback_mock,
    )

    # Проверяем, что callback была вызвана 100 раз с ключевым словом "word2"
    expected_calls = [mocker.call(required_fields[i], "WORd2") for i in range(100)]
    assert callback_mock.call_args_list == expected_calls


def test_parse_json_multiple_case_insensetive_keywords_only_req_fields(mocker):
    # Регистрозависимые req fields с несколькими совпадающими
    # регистрозависимыми ключевыми словами
    callback_mock = mocker.Mock()

    data = {f"key{i}": "Word{i} WORd2 wORDIK3 rAP4" for i in range(100)}
    json_str = json.dumps(data)
    required_fields = [f"key{i}" for i in range(50)]
    required_fields.extend([f"KeY{i}" for i in range(50)])
    keywords = ["worD2", "Rap4"]
    # keywords = ["worD2"]

    parse_json(
        json_str,
        required_fields=required_fields,
        keywords=keywords,
        keyword_callback=callback_mock,
    )

    # Проверяем, что callback была вызвана 100 раз с ключевым словом "worD2" и "rAP4"
    expected_calls = [
        mocker.call(required_fields[i], word)
        for i in range(50)
        for word in ["WORd2", "rAP4"]
    ]

    assert callback_mock.call_args_list == expected_calls


def test_parse_json_multiple_keywords_in_req_field(mocker):
    # Регистрозависимые совпдания keyword в одной строке
    callback_mock = mocker.Mock()

    json_str = '{"key1": "Word1 woRd2 word3 wOrd2 WORD2 word4 word2", \
                "key2": "woRd2 wOrd2 word3 WORD2 word2"}'
    required_fields = ["key1"]
    keywords = ["word2"]

    parse_json(
        json_str,
        required_fields=required_fields,
        keywords=keywords,
        keyword_callback=callback_mock,
    )

    # Проверяем, что callback была вызвана для каждого нужного keyword
    expected_calls = [
        mocker.call("key1", "woRd2"),
        mocker.call("key1", "wOrd2"),
        mocker.call("key1", "WORD2"),
        mocker.call("key1", "word2"),
    ]

    assert callback_mock.call_args_list == expected_calls
