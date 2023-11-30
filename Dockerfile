FROM python:3.12-slim as builder

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .
COPY README.md .

COPY fastapi_example ./fastapi_example

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-ansi

COPY settings.toml .
COPY .secrets.toml .

# Create the app user
RUN groupadd app && useradd -g app app
RUN chown -R app:app /app
USER app

CMD ["uvicorn", "fastapi_example.app:app", "--host=0.0.0.0","--port=8000","--reload"]
