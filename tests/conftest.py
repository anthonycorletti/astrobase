import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from typer.testing import CliRunner

from astrobase.cli.main import app
from astrobase.server.main import api

runner = CliRunner()


@pytest.fixture(scope="session")
def client() -> Generator:
    with TestClient(api) as client:
        yield client


@pytest.fixture(scope="function")
def astrobase_profile() -> Generator:
    name = "test-profile"
    os.environ["ASTROBASE_PROFILE_NAME"] = name
    runner.invoke(app, ["profile", "create", name])
    yield
    runner.invoke(app, ["profile", "delete", name])
