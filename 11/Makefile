.PHONY: all clean venv install test

all: venv install

venv:
	python3 -m venv venv
	. venv/bin/activate && pip install -r ../requirements/11.txt

install:
	. venv/bin/activate && python setup.py install

test:
	. venv/bin/activate && pytest

coverage:
	. venv/bin/activate && coverage run -m pytest && coverage report

main:
	clear && . venv/bin/activate && python3 main.py

clean:
	rm -rf venv build dist cjson.cpython-*.so
