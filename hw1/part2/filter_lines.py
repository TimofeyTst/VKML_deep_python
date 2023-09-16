def filter_lines(file_path: str, search_words: list):
    """
    Генерирует строку, если она содержит слова из списка в любом регистре.

    Аргументы:
    file_path (str): Строка, в которой указываем путь до файла,
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
    # Открываем файл для чтения
    with open(file_path, "r", encoding="utf-8") as file:
        # Приводим слова к нижнему регистру
        search_words = set(word.lower() for word in search_words)

        for line in file:
            # Разбиваем строку на слова и приводим их к нижнему регистру
            words = line.strip().lower().split()

            # Если слово попадает в список, то отдаем строку
            if any(word in search_words for word in words):
                yield line
