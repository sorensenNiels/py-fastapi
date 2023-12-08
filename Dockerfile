# ------------------------------------------------------------------------
# PY-BUILDER
# ------------------------------------------------------------------------
FROM python:3.12-bookworm as py-builder

ARG POETRY_VERSION=1.7.1

# Install OS packages for building
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends build-essential

# Install Poetry
RUN pip install poetry==${POETRY_VERSION}

# Setup Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Set working directory
WORKDIR /app

# Create dummy README.md to prevent poetry from failing
RUN touch README.md

# Copy required files for building
COPY pyproject.toml poetry.lock ./

# RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-ansi --no-root && rm -rf $POETRY_CACHE_DIR

# ------------------------------------------------------------------------
# PY-RUNTIME
# ------------------------------------------------------------------------
FROM python:3.12-slim-bookworm as py-runtime

ARG WORK_DIR=app

# Setup path to virtual environment
ENV VIRTUAL_ENV=/${WORK_DIR}/.venv 
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

# Create the app user and home folder
RUN groupadd app && useradd -g app app
RUN mkdir /home/app && chown -R app:app /home/app

WORKDIR /${WORK_DIR}

# Create data folder
RUN mkdir /${WORK_DIR}/data && chown -R app:app /${WORK_DIR}/data

# Get the dependencies from build step
COPY --from=py-builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Provide required files for runtime
COPY fastapi_example ./fastapi_example
COPY config ./config
# COPY settings.toml .
# COPY .secrets.toml .

# entrypoint using gunicorn (multi workers)
# RUN echo "#!/bin/sh" > entrypoint.sh
# RUN echo "gunicorn fastapi_example.app:app --workers=5 --worker-class=uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 --access-logfile -" >> entrypoint.sh
# RUN chmod +x entrypoint.sh

# entrypoint using uvicorn (one worker)
RUN echo "#!/bin/sh" > entrypoint.sh
RUN echo "uvicorn fastapi_example.app:app --host=0.0.0.0 --port=8000"  >> entrypoint.sh
RUN chmod +x entrypoint.sh

USER app

EXPOSE 8000
VOLUME [ "${WORK_DIR}/data" ]

CMD [ "./entrypoint.sh" ]
