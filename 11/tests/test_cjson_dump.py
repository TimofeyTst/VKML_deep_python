import json
import cjson

import pytest


def test_json_dump_invalid_type():
    uncorrect_formats = [
        12312312,
        '"asdasd": value"',
        '{"asdasd": value"}',
        ("key", "value"),
    ]

    for uncorrect_format in uncorrect_formats:
        with pytest.raises(TypeError, match="Expected dictionary"):
            cjson.dumps(uncorrect_format)


def test_json_dump_invalid_key_type():
    uncorrect_formats = [
        {(1, 2, 3): "val"},
        {(1, 2, 3): 15},
        {1.15: "val"},
        {15: "val"},
    ]

    for uncorrect_format in uncorrect_formats:
        with pytest.raises(TypeError, match="Invalid key type"):
            cjson.dumps(uncorrect_format)


def test_json_dump_invalid_value_type():
    uncorrect_formats = [
        {"val": (1, 2, 3)},
        {"15": (1, 2, 3)},
        {"val": 1.15},
    ]

    for uncorrect_format in uncorrect_formats:
        with pytest.raises(TypeError, match="Invalid value type"):
            cjson.dumps(uncorrect_format)


def test_json_dump_valid_value_type():
    correct_formats = [
        {"val": 1},
        {"15": "(1,2,3)"},
        {"val": 1238},
    ]

    for correct_format in correct_formats:
        json_res = json.dumps(correct_format)
        cjson_res = cjson.dumps(correct_format)
        assert json_res == cjson_res
