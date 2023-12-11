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

.PHONY: clean
clean:            ## Clean unused files.
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build

.PHONY: virtualenv
virtualenv:       ## Create a virtual environment.
	poetry install

.PHONY: release
release:          ## Create a new tag for release.
	@echo "WARNING: This operation will create s version tag and push to github"
	@read -p "Version? (provide the next x.y.z semver) : " TAG
	@echo "creating git tag : $${TAG}"
	@git tag $${TAG}
	@echo "$${TAG}" > ${PACKAGE_NAME}/VERSION
	@$(ENV_PREFIX)gitchangelog > HISTORY.md
	@git add ${PACKAGE_NAME}/VERSION HISTORY.md
	@git commit -m "release: version $${TAG} 🚀"
	@git push -u origin HEAD --tags
	@echo "Github Actions will detect the new tag and release the new version."

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
	uvicorn fastapi_example.app:app

start-gunicorn:
	echo "Starting FastAPI using gunicorn "
	gunicorn fastapi_example.app:app --workers=2 --worker-class=uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 --access-logfile -

docker-build:
	echo "Building local docker image"
	docker build -t fastapi_example --build-arg POETRY_VERSION=${POETRY_VERSION} .

docker-build-alpine:
	echo "Building local docker image (alpine)"
	docker build -t fastapi_example_alpine --build-arg POETRY_VERSION=${POETRY_VERSION} -f ./Dockerfile.alpine .

docker-run:
	echo "Run local docker container"
	@-docker volume create --name=fastapi_example
	docker run -it --rm -v fastapi_example:/app/data -p 8000:8000 fastapi_example

docker-run-alpine:
	echo "Run local docker container"
	@-docker volume create --name=fastapi_example
	docker run -it --rm -v fastapi_example:/app/data -p 8000:8000 fastapi_example_alpine


postgresql:
	docker run --name postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres

redis:
	docker run --name redis -p 6379:6379 -d redis