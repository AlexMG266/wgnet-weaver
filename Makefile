# Variables
VENV=venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip
CONFIG_DIR=configs
DB_FILE=~/.wgnet-weaver.db
PYCACHE=$(shell find . -name "__pycache__")

venv:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip

install: venv
	$(PIP) install -r requirements.txt

test:
	$(PYTHON) -m unittest discover -s tests

run:
	$(PYTHON) -m cli.wgnet $(ARGS)

# Limpieza de cachés de Python
clean:
	@echo "[*] Cleaning Python cache..."
	@rm -rf $(PYCACHE)

clean-all: clean
	@echo "[*] Removing generated configuration files..."
	@rm -rf $(CONFIG_DIR)
	@echo "[*] Removing database..."
	@rm -f $(DB_FILE)
	@echo "[*] Removing virtual environment..."
	@rm -rf $(VENV)
	@echo "[*] All cleaned!"
