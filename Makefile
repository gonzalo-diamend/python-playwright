.PHONY: setup test

setup:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt
	. .venv/bin/activate && playwright install

test:
	. .venv/bin/activate && pytest
