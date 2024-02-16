SHELL := env PYTHON_VERSION=$(PYTHON_VERSION) /bin/bash
.SILENT: install test lint format
PYTHON_VERSION ?= 3.10

install:
	curl -sSf https://rye-up.com/get | RYE_NO_AUTO_INSTALL=1 RYE_INSTALL_OPTION="--yes" bash
	rye sync --no-lock --no-dev

devinstall:
	curl -sSf https://rye-up.com/get | RYE_NO_AUTO_INSTALL=1 RYE_INSTALL_OPTION="--yes" bash
	$(RYE_HOME)/rye pin $(PYTHON_VERSION)
	$(RYE_HOME)/rye sync

test:
	$(RYE_HOME)/rye run pytest tests/

lint:
	$(RYE_HOME)/rye run pylint ./game 

format:
	$(RYE_HOME)/rye run yapf --in-place --recursive main.py ./tests ./game

run:
	$(RYE_HOME)/rye run alex  # rethink this
	
all: install-dev lint test