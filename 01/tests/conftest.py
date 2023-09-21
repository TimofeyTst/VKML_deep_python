import os
import tempfile
import pytest


# Создаем временный файл для тестов
@pytest.fixture
def temp_file():
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "test_file.txt")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("а Роза упала на лапу Азора\n")
        file.write("Это просто текст\n")
        file.write("Неважно что я тут напишу, это тест\n")
    yield file_path
    os.remove(file_path)
