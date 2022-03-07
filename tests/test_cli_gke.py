from typing import Generator

from typer.testing import CliRunner

from astrobase.cli.main import app
from tests.factories import TEST_ASSET_DIR


def test_cluster_gke_create(
    astrobase_cli_runner: CliRunner, astrobase_server: Generator
) -> None:
    result = astrobase_cli_runner.invoke(
        app,
        [
            "cluster",
            "gke",
            "create",
            "--project-id",
            "my-test-project",
            "-f",
            f"{TEST_ASSET_DIR}/simple-gke.yaml",
        ],
    )
    assert result.exit_code == 0


def test_cluster_gke_delete(
    astrobase_cli_runner: CliRunner, astrobase_server: Generator
) -> None:
    result = astrobase_cli_runner.invoke(
        app,
        [
            "cluster",
            "gke",
            "delete",
            "--project-id",
            "my-test-project",
            "-f",
            f"{TEST_ASSET_DIR}/simple-gke.yaml",
        ],
    )
    assert result.exit_code == 0