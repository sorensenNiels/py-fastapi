# PY-BUILDER
FROM python:3.12-bookworm as py-builder

# Install OS packages for building
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends build-essential

# Install Poetry
RUN pip install poetry

# Set working directory
WORKDIR /app

# Create dummy README.md to prevent poetry from failing
RUN touch README.md

# Copy required files for building
COPY pyproject.toml .
COPY poetry.lock .
COPY fastapi_example ./fastapi_example

# RUN poetry config virtualenvs.create false
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-dev --no-interaction --no-ansi

# PY-RUNTIME
FROM python:3.12-slim-bookworm as py-runtime

# Install OS packages for production
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <packages>

WORKDIR /app

COPY settings.toml .
COPY .secrets.toml .

COPY --from=py-builder /app .

# Create the app user
RUN groupadd app && useradd -g app app
RUN chown -R app:app /app
USER app

EXPOSE 8000

# CMD [".venv/bin/uvicorn", "fastapi_example.app:app", "--host=0.0.0.0","--port=8000"]
CMD [".venv/bin/gunicorn", "fastapi_example.app:app", "--workers=1", "--worker-class=uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
