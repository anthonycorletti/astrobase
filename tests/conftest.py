import os
from typing import Any, Dict, Generator
from unittest.mock import patch

import boto3
import pytest
from starlette.testclient import TestClient

from astrobase.server.main import api


@pytest.fixture(scope="session")
def client() -> Generator:
    with TestClient(api) as client:
        yield client


@pytest.fixture(scope="session")
def eks_mock() -> Generator:
    os.environ["AWS_REGION"] = "us-east-1"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    os.environ["AWS_ACCESS_KEY_ID"] = "foo"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "bar"
    os.environ.pop("AWS_PROFILE", None)

    eks_client = boto3.client("eks")

    def eks_func(*args: Any, **kwargs: Dict[str, Any]) -> Any:
        return eks_client

    with patch("astrobase.providers.eks.boto3.client", eks_func):
        yield eks_func
