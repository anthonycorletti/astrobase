import os
import time
from multiprocessing import Process
from typing import Any, Dict, Generator
from unittest.mock import patch

import boto3
import pytest
from fastapi.testclient import TestClient
from typer.testing import CliRunner

from astrobasecloud.cli.main import app
from astrobasecloud.server.main import api


@pytest.fixture(scope="session")
def client() -> Generator:
    with TestClient(app=api) as client:
        yield client


@pytest.fixture(scope="function")
def astrobase_cli_runner() -> Generator:
    runner = CliRunner()
    test_config = f"{os.getcwd()}/config.json.test"
    os.environ["ASTROBASE_CONFIG"] = test_config
    name = "test-profile"
    runner.invoke(
        app,
        ["profile", "create", name, "--no-secure"],
    )
    os.environ["ASTROBASE_PROFILE_NAME"] = name
    yield runner
    runner.invoke(app, ["profile", "delete", name])
    os.remove(test_config)


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

    with patch("astrobasecloud.providers.aws.boto3.client", mock_eks):
        yield mock_eks


@pytest.fixture(scope="module")
def astrobase_server() -> Generator:
    runner = CliRunner()
    p = Process(
        target=runner.invoke,
        args=(app, ["server"]),
        daemon=True,
    )  # type: ignore
    p.start()
    time.sleep(3)
    yield
    p.terminate()
