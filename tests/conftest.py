from typing import Generator

import pytest
from fastapi.testclient import TestClient

from astrobase.server.main import api


@pytest.fixture(scope="session")
def client() -> Generator:
    with TestClient(api) as client:
        yield client
