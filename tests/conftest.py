import os
from typing import Any, Dict, Generator
from unittest.mock import patch

import boto3
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


@pytest.fixture(scope="session")
def mock_eks_client() -> Generator:
    os.environ["AWS_REGION"] = "us-east-1"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    os.environ["AWS_ACCESS_KEY_ID"] = "foo"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "bar"
    os.environ.pop("AWS_PROFILE", None)

    eks_client = boto3.client("eks")

    def mock_eks(*args: Any, **kwargs: Dict[str, Any]) -> Any:
        return eks_client

    with patch("astrobase.providers.aws.boto3.client", mock_eks):
        yield mock_eks
