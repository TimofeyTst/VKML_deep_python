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
    assert json_str == cjson.dumps(cjson.loads(json_str))


def test_json_dump_load():
    json_str = '{"old_year": 2023, "new_year": "2024"}'
    json_doc = json.loads(json_str)
    ujson_doc = ujson.loads(json_str)
    cjson_doc = cjson.loads(json_str)

    assert json_doc == ujson_doc == cjson_doc
    # cjson - cjson
    assert json_str == cjson.dumps(cjson.loads(json_str))

    # json - cjson
    assert json_str == cjson.dumps(json.loads(json_str))

    # ujson - cjson
    assert json_str == cjson.dumps(ujson.loads(json_str))


def test_json_load_dump():
    json_str = '{"old_year": 2023, "new_year": "2024"}'
    json_doc = json.loads(json_str)
    ujson_doc = ujson.loads(json_str)
    cjson_doc = cjson.loads(json_str)

    assert json_doc == ujson_doc == cjson_doc
    # cjson - cjson
    assert json_str == cjson.dumps(cjson.loads(json_str))

    # json - cjson
    assert json_str == json.dumps(cjson.loads(json_str))

    # ujson - cjson
    # ujson формирует строку без пробелов
    ujson_res = json_str.replace(" ", "")
    assert ujson_res == ujson.dumps(cjson.loads(json_str))


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

    assert json_str == cjson.dumps(cjson_doc)


def test_json_load_types_skipping_spaces():
    json_str = '{"old_year":2023,"new_year":"2024",     "france"   :   165   ,   "en"  :  "no", "rap":12  }'
    json_res = (
        '{"old_year": 2023, "new_year": "2024", "france": 165, "en": "no", "rap": 12}'
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

    assert json_res == cjson.dumps(cjson_doc)


def test_json_load_empty():
    json_str = "{ }"
    json_doc = json.loads(json_str)
    ujson_doc = ujson.loads(json_str)
    cjson_doc = cjson.loads(json_str)

    assert json_doc == ujson_doc
    assert json_doc == ujson_doc == cjson_doc

    # Проверяем, что результат пустой словарь
    assert isinstance(json_doc, dict)
    assert len(cjson_doc) == 0


def test_json_load_empty_skip_spaces():
    json_str = "{         }"
    json_doc = json.loads(json_str)
    ujson_doc = ujson.loads(json_str)
    cjson_doc = cjson.loads(json_str)

    assert json_doc == ujson_doc
    assert json_doc == ujson_doc == cjson_doc

    # Проверяем, что результат пустой словарь
    assert isinstance(json_doc, dict)
    assert len(cjson_doc) == 0


def test_json_load_repeated_keys():
    json_str = '{"name": "artem", "name": "12389", "name": 544 }'
    json_doc = json.loads(json_str)
    ujson_doc = ujson.loads(json_str)
    cjson_doc = cjson.loads(json_str)

    assert json_doc == ujson_doc
    assert json_doc == ujson_doc == cjson_doc
