.ONESHELL:
POETRY_VERSION=1.7.1

docker-build-fastapi_example:
	echo "Building local docker image"
	docker build -t fastapi_example --build-arg POETRY_VERSION=${POETRY_VERSION} -f Dockerfile.fastapi_example .


docker-run-fastapi_example:
	echo "Run local docker container"
	@-docker volume create --name=fastapi_example
	docker run -it --rm -v fastapi_example:/app/data -p 8000:8000 fastapi_example

postgresql:
	docker run --name postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres

redis:
	docker run --name redis -p 6379:6379 -d redis