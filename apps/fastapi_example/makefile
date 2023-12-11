.ONESHELL:
ENV_PREFIX=$(shell python -c "if __import__('pathlib').Path('.venv/bin/pip').exists(): print('.venv/bin/')")
PACKAGE_NAME=fastapi_example
POETRY_VERSION=1.7.1

.PHONY: show
show:             ## Show the current environment.
	@echo "Current environment for ${PACKAGE_NAME}:"
	poetry env info

.PHONY: install
install:          ## Install the project in dev mode.
	poetry install

.PHONY: update
update:
	poetry update

.PHONY: fmt
fmt:              ## Format code using black & isort.
	$(ENV_PREFIX)isort ${PACKAGE_NAME}/
	$(ENV_PREFIX)black -l 79 ${PACKAGE_NAME}/
	$(ENV_PREFIX)black -l 79 tests/

.PHONY: lint
lint:             ## Run pep8, black, mypy linters.
	$(ENV_PREFIX)flake8 ${PACKAGE_NAME}/
	$(ENV_PREFIX)black -l 79 --check ${PACKAGE_NAME}/
	$(ENV_PREFIX)black -l 79 --check tests/
	$(ENV_PREFIX)mypy --ignore-missing-imports ${PACKAGE_NAME}/

.PHONY: test
test: lint        ## Run tests and generate coverage report.
	$(ENV_PREFIX)pytest -v --cov-config .coveragerc --cov=${PACKAGE_NAME} -l --tb=short --maxfail=1 tests/
	$(ENV_PREFIX)coverage xml
	$(ENV_PREFIX)coverage html

.PHONY: watch
watch:            ## Run tests on every change.
	ls **/**.py | entr $(ENV_PREFIX)pytest --picked=first -s -vvv -l --tb=long --maxfail=1 tests/

.PHONY: virtualenv
virtualenv:       ## Create a virtual environment.
	poetry install

.PHONY: docs
docs:             ## Build the documentation.
	@echo "building documentation ..."
	@$(ENV_PREFIX)mkdocs build
	URL="site/index.html"; xdg-open $$URL || sensible-browser $$URL || x-www-browser $$URL || gnome-open $$URL  || open $$URL

.PHONY: shell
shell:            ## Open a shell in the project.
	poetry shell

start: 
	echo "Starting FastAPI"
	-@mkdir data
	uvicorn fastapi_example.app:app
