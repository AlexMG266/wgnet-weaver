# Variables
VENV=venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

venv:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip

install: venv
	$(PIP) install -r requirements.txt

test:
	$(PYTHON) -m unittest discover -s tests

run:
	$(PYTHON) -m cmd.netweaver $(ARGS)
