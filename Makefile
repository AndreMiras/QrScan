VENV_NAME=venv
ACTIVATE_PATH=$(VENV_NAME)/bin/activate
PIP=$(VENV_NAME)/bin/pip
TOX=`. $(ACTIVATE_PATH); which tox`
GARDEN=`. $(ACTIVATE_PATH); which garden`
PYTHON=$(VENV_NAME)/bin/python
ISORT=$(VENV_NAME)/bin/isort
FLAKE8=$(VENV_NAME)/bin/flake8
SOURCES=src/
SYSTEM_DEPENDENCIES= \
	libzbar-dev \
	virtualenv
OS=$(shell lsb_release -si)


all: system_dependencies virtualenv

venv:
	virtualenv -p python3 venv

virtualenv: venv
	$(PIP) install Cython==0.26.1
	$(PIP) install -r requirements.txt
	$(GARDEN) install xcamera

virtualenv-test: virtualenv
	$(PIP) install -r requirements/requirements-test.txt

system_dependencies:
ifeq ($(OS), Ubuntu)
	sudo apt install --yes --no-install-recommends $(SYSTEM_DEPENDENCIES)
endif

clean:
	rm -rf venv/ .tox/

isort-check: virtualenv-test
	$(ISORT) --check-only --recursive --diff $(SOURCES)

isort-fix: virtualenv-test
	$(ISORT) --recursive $(SOURCES)

flake8: virtualenv-test
	$(FLAKE8) $(SOURCES)

lint: isort-check flake8

test: virtualenv-test lint
	$(PYTHON) -m unittest discover --start-directory=src/
