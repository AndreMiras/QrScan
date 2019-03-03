VENV_NAME=venv
ACTIVATE_PATH=$(VENV_NAME)/bin/activate
PIP=$(VENV_NAME)/bin/pip
TOX=`. $(ACTIVATE_PATH); which tox`
GARDEN=`. $(ACTIVATE_PATH); which garden`
PYTHON=$(VENV_NAME)/bin/python
SYSTEM_DEPENDENCIES= \
	libzbar-dev \
	virtualenv
OS=$(shell lsb_release -si)


all: system_dependencies virtualenv

virtualenv:
	test -d venv || virtualenv -p python3 venv
	. venv/bin/activate
	$(PIP) install Cython==0.26.1
	$(PIP) install -r requirements.txt
	$(GARDEN) install xcamera

system_dependencies:
ifeq ($(OS), Ubuntu)
	sudo apt install --yes --no-install-recommends $(SYSTEM_DEPENDENCIES)
endif

clean:
	rm -rf venv/ .tox/

test:
	$(TOX)
