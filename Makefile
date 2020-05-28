VIRTUAL_ENV ?= venv
ACTIVATE_PATH=$(VIRTUAL_ENV)/bin/activate
PIP=$(VIRTUAL_ENV)/bin/pip
PYTHON=$(VIRTUAL_ENV)/bin/python
ISORT=$(VIRTUAL_ENV)/bin/isort
FLAKE8=$(VIRTUAL_ENV)/bin/flake8
TWINE=`which twine`
SOURCES=src/ setup.py
SYSTEM_DEPENDENCIES= \
	libzbar-dev \
	virtualenv
PYTHON_VERSION=3.8
PYTHON_WITH_VERSION=python$(PYTHON_VERSION)


all: system_dependencies virtualenv

$(VIRTUAL_ENV):
	$(PYTHON_WITH_VERSION) -m venv $(VIRTUAL_ENV)

virtualenv: $(VIRTUAL_ENV)
	$(PIP) install Cython==0.28.6
	$(PIP) install -r requirements.txt

virtualenv/test: virtualenv
	$(PIP) install -r requirements/requirements-test.txt

system_dependencies:
	apt install --yes --no-install-recommends $(SYSTEM_DEPENDENCIES)

run/linux: virtualenv
	# The `--debug` flag is required if you want to see errors printed in your console.
	# Otherwise the exception will be only sent to Sentry.
	# $(PYTHON) src/qrscan/main.py --debug
	$(PYTHON) src/main.py --debug

run: run/linux

lint/isort-check: virtualenv/test
	$(ISORT) --check-only --recursive --diff $(SOURCES)

lint/isort-fix: virtualenv/test
	$(ISORT) --recursive $(SOURCES)

lint/flake8: virtualenv/test
	$(FLAKE8) $(SOURCES)

lint: lint/isort-check lint/flake8

test: virtualenv/test lint
	$(PYTHON) -m unittest discover --start-directory=src/

release/clean:
	rm -rf dist/ build/

release/build: release/clean
	$(PYTHON) setup.py sdist bdist_wheel
	$(TWINE) check dist/*

release/upload:
	$(TWINE) upload dist/*

clean: release/clean
	py3clean src/
	find src/ -type d -name "__pycache__" -exec rm -r {} +
	find src/ -type d -name "*.egg-info" -exec rm -r {} +

clean/venv: clean
	rm -rf $(VIRTUAL_ENV)

clean/all: clean clean/venv
