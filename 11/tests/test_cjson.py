import json
import ujson
import cjson


def test_json_load():
    json_str = '{"old_year": 2023, "new_year": "2024"}'
    json_doc = json.loads(json_str)
    ujson_doc = ujson.loads(json_str)
    cjson_doc = cjson.loads(json_str)

    assert json_doc == ujson_doc
    assert json_doc == ujson_doc == cjson_doc
    # assert json_str == cjson.dumps(cjson.loads(json_str))


def test_json_load_types():
    json_str = '{"old_year": 2023, "new_year": "2024"}'
    json_doc = json.loads(json_str)
    ujson_doc = ujson.loads(json_str)
    cjson_doc = cjson.loads(json_str)

    assert json_doc == ujson_doc
    assert json_doc == ujson_doc == cjson_doc

    assert all(isinstance(key, str) for key in cjson_doc.keys())

    # Проверяем типы значений
    assert isinstance(cjson_doc["old_year"], int)
    assert isinstance(cjson_doc["new_year"], str)


def test_json_load_types_skipping_spaces():
    json_str = (
        '{"old_year": 2023, "new_year": "2024",     "france"   : 165, "en" : "no"}'
    )
    json_doc = json.loads(json_str)
    ujson_doc = ujson.loads(json_str)
    cjson_doc = cjson.loads(json_str)

    assert json_doc == ujson_doc
    assert json_doc == ujson_doc == cjson_doc

    assert all(isinstance(key, str) for key in cjson_doc.keys())

    # Проверяем типы значений
    assert isinstance(cjson_doc["old_year"], int)
    assert isinstance(cjson_doc["new_year"], str)
    assert isinstance(cjson_doc["france"], int)
    assert isinstance(cjson_doc["en"], str)
