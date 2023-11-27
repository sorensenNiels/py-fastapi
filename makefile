prod-dependencies:
	pip install -r requirements.txt

dev-dependencies:
	pip install -r requirements-dev.txt

dependencies: prod-dependencies dev-dependencies

start:
	cd py_fastapi && uvicorn py_fastapi.app:app --reload

postgresql:
	docker run --name postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres

redis:
	docker run --name redis -p 6379:6379 -d redis