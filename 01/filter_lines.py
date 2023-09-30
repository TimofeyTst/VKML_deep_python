def filter_lines(file, search_words: list):
    """
    Генерирует строку, если она содержит слова из списка в любом регистре.

    Аргументы:
    file: str или файловый объект. Если это строка,
    то это путь до файла, иначе - файловый объект.
    search_words (list): Список, в котором ищем совпадение слов.

    Возвращает:
    str: Строка из файла, в которой содержится хотя бы одно из переданных слов.

    Примечания:
    - Все строки search_words будут приведены к нижнему регистру.

    Пример использования:
    >>> file_path = 'data/file.txt'
    >>> search_words = ['роза', 'азора']
    >>> for result in filter_lines(file_path, search_words):
    ...     print(result)
    а Роза упала на лапу Азора
    """
    if isinstance(file, str):
        file = open(file, "r", encoding="utf-8")
        close_file = True
    else:
        close_file = False

    try:
        # Приводим слова к нижнему регистру
        search_words = set(word.lower() for word in search_words)

        for line in file:
            # Разбиваем строку на слова и приводим их к нижнему регистру
            words = line.strip().lower().split()

            # Если слово попадает в список, то отдаем строку
            if any(word in search_words for word in words):
                yield line
    finally:
        # Если был открыт файл внутри функции, закрываем его
        if close_file:
            file.close()
