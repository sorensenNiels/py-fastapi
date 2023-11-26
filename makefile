prod-dependencies:
	pip install -r requirements.txt

dev-dependencies:
	pip install -r requirements-dev.txt

dependencies: prod-dependencies dev-dependencies

start:
	uvicorn app:app --reload
