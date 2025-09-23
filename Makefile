# Variables
VENV=venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip
CONFIG_DIR=configs

# Directorios en $HOME
BASE_DIR=$(HOME)/.wgnet-weaver
DB_FILE=$(BASE_DIR)/db.sqlite3
CONFIGS_DIR=$(BASE_DIR)/configs
INVENTORIES_DIR=$(BASE_DIR)/inventories
PLAYBOOKS_DIR=$(BASE_DIR)/playbooks
LOGS_DIR=$(BASE_DIR)/logs
STATE_FILE=$(BASE_DIR)/state.json

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
	@echo "[*] Removing application data..."
	@rm -rf $(BASE_DIR)
	@echo "[*] Removing virtual environment..."
	@rm -rf $(VENV)
	@echo "[*] All cleaned!"
