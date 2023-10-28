import json


def parse_json(
    json_str: str, required_fields=None, keywords=None, keyword_callback=None
):
    """
    Функция, должна принимать строку, в которой содержится json,
    и произвести парсинг этого json. Упростим немного и представим,
    что json представляет из себя только коллекцию ключей-значений.
    Причём ключами и значениями являются только строки.
    """
    if not json_str:
        raise ValueError("json_str cannot be empty")

    if not required_fields or not keywords:
        raise ValueError("required_fields and keywords cannot be empty")

    # Преобразуем keywords к нижнему регистру и удалим дубликаты
    keywords = set(keyword.lower() for keyword in keywords)

    json_doc = json.loads(json_str)
    for field, words in json_doc.items():
        if field not in required_fields:
            continue

        # Если слово содержится в required_fields, то обрабатываем words
        for word in words.split():
            if word.lower() in keywords:
                # Если определен keyword_callback
                if keyword_callback:
                    keyword_callback(field, word)
