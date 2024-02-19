SHELL := env PYTHON_VERSION=$(PYTHON_VERSION) /bin/bash
.SILENT: install test lint format
PYTHON_VERSION ?= 3.10

install:
	curl -sSf https://rye-up.com/get | RYE_NO_AUTO_INSTALL=1 RYE_INSTALL_OPTION="--yes" bash
	$(HOME)/.rye/shims/rye sync --no-lock --no-dev

devinstall:
	curl -sSf https://rye-up.com/get | RYE_NO_AUTO_INSTALL=1 RYE_INSTALL_OPTION="--yes" bash
	$(HOME)/.rye/shims/rye pin $(PYTHON_VERSION)
	$(HOME)/.rye/shims/rye sync --no-lock

test:
	$(HOME)/.rye/shims/rye run pytest tests/

lint:
	$(HOME)/.rye/shims/rye lint --fix 

format:
	$(HOME)/.rye/shims/rye fmt

all: devinstall lint format test