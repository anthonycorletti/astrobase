from typing import Generator

from typer.testing import CliRunner

from astrobasecloud.cli.main import app
from tests.factories import TEST_ASSET_DIR


def test_cluster_eks_create(
    astrobase_cli_runner: CliRunner, astrobase_server: Generator
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


def test_cluster_eks_delete(
    astrobase_cli_runner: CliRunner, astrobase_server: Generator
) -> None:
    result = astrobase_cli_runner.invoke(
        app,
        [
            "cluster",
            "eks",
            "delete",
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
