from typing import Generator
from unittest import mock

from typer.testing import CliRunner

from astrobasecloud.cli.main import app
from tests.factories import TEST_ASSET_DIR
from tests.mocks import MockJsonResponse


@mock.patch("requests.post", return_value=MockJsonResponse(response={"mock": "value"}))
def test_cluster_eks_create(
    mock_request_post: mock.MagicMock,
    astrobase_cli_runner: CliRunner,
    astrobase_server: Generator,
) -> None:
    result = astrobase_cli_runner.invoke(
        app,
        [
            "cluster",
            "eks",
            "create",
            "--kubernetes-control-plane-arn",
            "arn:aws:iam::000000000001:role/AstrobaseEKSClusterRole",
            "--cluster-subnet-id",
            "subnet-000001",
            "--cluster-subnet-id",
            "subnet-000002",
            "--cluster-security-group-id",
            "sg-000001",
            "--nodegroup-noderole-mapping",
            "main=arn:aws:iam::541181908229:role/AstrobaseEKSNodegroupRole",
            "-f",
            f"{TEST_ASSET_DIR}/simple-eks.yaml",
        ],
    )
    assert result.exit_code == 0


@mock.patch(
    "requests.delete", return_value=MockJsonResponse(response={"mock": "value"})
)
def test_cluster_eks_delete(
    mock_request_delete: mock.MagicMock,
    astrobase_cli_runner: CliRunner,
    astrobase_server: Generator,
) -> None:
    result = astrobase_cli_runner.invoke(
        app,
        [
            "cluster",
            "eks",
            "delete",
            "--cluster-name",
            "my-eks-cluster",
            "--region",
            "us-east-1",
            "--nodegroup-names",
            "default",
        ],
    )
    assert result.exit_code == 0
