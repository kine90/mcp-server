VENV?=.venv
PY=$(VENV)/bin/python
PIP=$(VENV)/bin/pip
PYTEST=$(VENV)/bin/pytest
RUFF=$(VENV)/bin/ruff
MYPY=$(VENV)/bin/mypy
FASTMCP=$(VENV)/bin/fastmcp
PRECOMMIT=$(VENV)/bin/pre-commit

.PHONY: init test test-integration lint format type hooks run coverage clean

$(VENV)/bin/python:
	python3.12 -m venv $(VENV)
	$(PY) -m pip install -U pip

init: $(VENV)/bin/python
	$(PIP) install -e .
	$(PIP) install ruff mypy pytest pre-commit

test: $(VENV)/bin/python
	$(PYTEST)

coverage: $(VENV)/bin/python
	$(PYTEST) --cov=meraki_mcp --cov-report=term-missing --cov-fail-under=60

test-integration: $(VENV)/bin/python
	$(PYTEST) -m integration -q

lint: $(VENV)/bin/python
	$(RUFF) check .

format: $(VENV)/bin/python
	$(RUFF) format .

type: $(VENV)/bin/python
	$(MYPY) .

hooks: $(VENV)/bin/python
	$(PRECOMMIT) install
	$(PRECOMMIT) run -a

run: $(VENV)/bin/python
	@if [ -z "$$MERAKI_API_KEY" ]; then echo "MERAKI_API_KEY not set"; exit 1; fi
	$(FASTMCP) run meraki_mcp/main.py:mcp

clean:
	rm -rf $(VENV) .pytest_cache .ruff_cache .mypy_cache
