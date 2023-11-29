poetry-environments:
	poetry env list

start:
	cd todo_fastapi && uvicorn todo_fastapi.app:app --reload

postgresql:
	docker run --name postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres

redis:
	docker run --name redis -p 6379:6379 -d redis