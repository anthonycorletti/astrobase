from typing import Generator
from unittest import mock

from typer.testing import CliRunner

from astrobasecloud.cli.main import app
from tests.factories import TEST_ASSET_DIR
from tests.mocks import MockJsonResponse


@mock.patch("requests.post", return_value=MockJsonResponse(response={"mock": "value"}))
def test_cluster_gke_create(
    mock_request_post: mock.MagicMock,
    astrobase_cli_runner: CliRunner,
    astrobase_server: Generator,
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


@mock.patch(
    "requests.delete", return_value=MockJsonResponse(response={"mock": "value"})
)
def test_cluster_gke_delete(
    mock_request_delete: mock.MagicMock,
    astrobase_cli_runner: CliRunner,
    astrobase_server: Generator,
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
