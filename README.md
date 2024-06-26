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
pytest 01 # or pytest path_name
```

```shell
coverage run -m pytest 01 # or coverage run -m pytest path_name for example
coverage report
```
## Лекции и материалы (слайды, домашки, код с занятий)
01. [Введение, типы данных, управляющие конструкции, тестирование](lesson-01)
### Homework 1
```shell
coverage run -m pytest 01/
coverage report
```
#### 01 Coverage
| Name               | Stmts | Miss | Cover |
|--------------------|------------|------|----------|
| 01/filter_lines.py               |   13 | 0 | 100% |
| 01/model.py                      |  10 | 0 | 100% |
| 01/predict_message.py            |  12 | 0 | 100% |
| TOTAL                            | 35 | 0 | 100% |


### Homework 2
```shell
coverage run -m pytest 02/
coverage report
```
#### 02 Coverage
| Name               | Stmts | Miss | Cover |
|--------------------|------------|------|----------|
| 02/mean.py            | 18         | 0    | 100%     |
| 02/parse.py           | 14         | 0    | 100%     |
| TOTAL              | 32        | 0    | 100%     |
