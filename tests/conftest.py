import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from astrobase.server.main import api


@pytest.fixture(scope="session")
def client() -> Generator:
    with TestClient(api) as client:
        yield client


@pytest.fixture(scope="function")
def astrobase_profile_name() -> str:
    name = "test-profile"
    os.environ["ASTROBASE_PROFILE_NAME"] = name
    return name
