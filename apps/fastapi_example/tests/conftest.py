import os
import sys

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError
from typer.testing import CliRunner

# This next line ensures tests uses its own database and settings environment
os.environ["FORCE_ENV_FOR_DYNACONF"] = "testing"  # noqa
# WARNING: Ensure imports from `ailab_apigateway` comes after this line
from ailab_apigateway import app, db, settings  # noqa
from ailab_apigateway.cli import cli, create_user  # noqa


# each test runs on cwd to its temp dir
@pytest.fixture(autouse=True)
def go_to_tmpdir(request):
    # Get the fixture dynamically by its name.
    tmpdir = request.getfixturevalue("tmpdir")
    # ensure local test created packages can be imported
    sys.path.insert(0, str(tmpdir))
    # Chdir only for the duration of the test.
    with tmpdir.as_cwd():
        yield


@pytest.fixture(scope="function", name="app")
def _app():
    return app


@pytest.fixture(scope="function", name="cli")
def _cli():
    return cli


@pytest.fixture(scope="function", name="settings")
def _settings():
    return settings


@pytest.fixture(scope="function")
def api_client():
    return TestClient(app)


@pytest.fixture(scope="function")
def api_client_authenticated():
    try:
        create_user("admin", "admin", superuser=True)
    except IntegrityError:
        pass

    client = TestClient(app)
    token = client.post(
        "/token",
        data={"username": "admin", "password": "admin"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    ).json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    return client


@pytest.fixture(scope="function")
def cli_client():
    return CliRunner()


def remove_db():
    # Remove the database file
    try:
        os.remove("testing.db")
    except FileNotFoundError:
        pass


@pytest.fixture(scope="session", autouse=True)
def initialize_db(request):
    db.create_db_and_tables(db.engine)
    request.addfinalizer(remove_db)
