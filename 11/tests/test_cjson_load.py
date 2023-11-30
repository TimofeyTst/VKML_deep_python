import cjson

import pytest


def test_json_load_invalid_type():
    uncorrect_formats = [12312312, {"key": 123, "value": 15}, ("key", "value")]

    for uncorrect_format in uncorrect_formats:
        with pytest.raises(TypeError, match="Invalid argument type"):
            cjson.loads(uncorrect_format)


def test_json_load_invalid_format():
    uncorrect_formats = [
        "str",
        '"asdasd',
        '"asdasd"',
        '"asdasd": 123',
        '"asdasd": 123',
        '{"asdasd": 123',
        '{"asdasd": value"',
        "{",
        "{ }{",
        "{ } {",
        "{ }:,",
    ]

    for uncorrect_format in uncorrect_formats:
        with pytest.raises(
            TypeError, match="Invalid JSON format: must start with '{' and end with '}'"
        ):
            cjson.loads(uncorrect_format)


def test_json_load_invalid_keys():
    uncorrect_formats = [
        "{ 'asdasd': 123}",
        "{ 500: 123 }",
        "{ some: 123 }",
        '{ some: "123" }',
        '{ 500: "123" }',
        "{ 'asdasd': \"123\"}",
        '{ "asdasd": 123, \'error\': "123" }',
        '{ "asdasd": "123", \'error\': "123" }',
        '{ "asdasd": "123", \'error\': "123", "normal": 500 }',
    ]

    for uncorrect_format in uncorrect_formats:
        with pytest.raises(
            TypeError,
            match="Error parse JSON key: must start with '\"' and end with '\"'",
        ):
            cjson.loads(uncorrect_format)


def test_json_load_invalid_key_value_delimeter():
    uncorrect_formats = [
        '{ "asdasd" 123}',
        '{ "500" - 123 }',
        '{ "some": 123, "test" "this" }',
        '{ "asdasd": "123", "norm": 600, "error" 19, "luck": "321"}',
    ]

    for uncorrect_format in uncorrect_formats:
        with pytest.raises(
            TypeError, match="Invalid JSON format: after key should be a ':'"
        ):
            cjson.loads(uncorrect_format)


def test_json_load_invalid_value_type():
    uncorrect_formats = [
        '{ "asdasd": "123\'}',
        '{ "500": \'123" }',
        '{ "some": "123\' }',
        '{ "some": { 123 } }',
        '{ "asdasd": "123", "norm": 600, "error": tuple(19), "luck": "321"}',
    ]

    for uncorrect_format in uncorrect_formats:
        with pytest.raises(TypeError, match="Error parse JSON value"):
            cjson.loads(uncorrect_format)


def test_json_load_invalid_json_format():
    uncorrect_formats = [
        '{ "asdasd": "123", "norm": 600  "error": 19, "luck": "321"}',
        '{ "asdasd": "123", "norm": 600, "error": 19 "luck": "321"}',
    ]

    for uncorrect_format in uncorrect_formats:
        with pytest.raises(TypeError, match="Invalid JSON format: expected ',' or '}'"):
            cjson.loads(uncorrect_format)


def test_json_load_invalid_json_closed_early():
    uncorrect_formats = [
        '{ "asdasd": "123"} "norm": 600  "error": 19, "luck": "321"}',
        '{ "asdasd": "123"} {"norm": 600  "error": 19, "luck": "321"}',
        '{ "asdasd": "123"} {"norm": 600}  {"error": 19}, {"luck": "321"} }',
    ]

    for uncorrect_format in uncorrect_formats:
        with pytest.raises(
            TypeError, match="Invalid JSON format: got '}' at not end of json string"
        ):
            cjson.loads(uncorrect_format)
