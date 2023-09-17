# VKML_deep_python
> Курс Углубленный Python от VK Education, осень 2023
### Старжевский Тимофей Евгеньевич ML-12
### Ментор: Оленников Вадим https://vk.com/vadimltd
## Platforms
- Linux Ubuntu 22.04
---

## Commands
### Requirements install
```shell
pip install -r requirements/dev.txt
```
### Linters
> ruff instead isort, autoflake
```shell
ruff --fix . # or ruff --fix hw1/part1 for example 
black . # or black hw1/part1 for example
```

Быстрое форматирование, если поддерживает среда
```shell
/bin/sh -e scripts/format
```

### Tests
```shell
pytest hw1/part1 # or pytest path_name
```

```shell
coverage run -m pytest hw1/part2 # or coverage run -m pytest path_name for example
coverage report
```
## Лекции и материалы (слайды, домашки, код с занятий)
01. [Введение, типы данных, управляющие конструкции, тестирование](lesson-01)
### Homework 1
#### Part 1 Coverage
| Name                                    | Stmts | Miss | Cover |
|-----------------------------------------|------------|------|----------|
| hw1/part1/model.py                      | 10         | 0    | 100%     |
| hw1/part1/predict_message.py            | 12         | 0    | 100%     |
| hw1/part1/tests/__init__.py             | 0          | 0    | 100%     |
| hw1/part1/tests/test_model.py           | 13         | 0    | 100%     |
| hw1/part1/tests/test_predict_message.py | 39         | 0    | 100%     |
| TOTAL                                   | 74         | 0    | 100%     |

#### Part 2 Coverage
| Name                                    | Stmts | Miss | Cover |
|-----------------------------------------|------------|------|----------|
| hw1/part2/filter_lines.py                | 7          | 0    | 100%     |
| hw1/part2/tests/__init__.py              | 0          | 0    | 100%     |
| hw1/part2/tests/conftest.py              | 13         | 0    | 100%     |
| hw1/part2/tests/test_filter_lines.py     | 15         | 0    | 100%     |
| TOTAL                                   | 35         | 0    | 100%     |


