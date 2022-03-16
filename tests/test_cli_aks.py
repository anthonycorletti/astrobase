from typing import Generator
from unittest import mock

from typer.testing import CliRunner

from astrobasecloud.cli.main import app
from tests.factories import TEST_ASSET_DIR


@mock.patch(
    "requests.post",
    return_value=mock.Mock(status_code=200, json=lambda: {"message": "Success!"}),
)
def test_cluster_aks_create(
    mock_azure_provider_post: mock.MagicMock,
    astrobase_cli_runner: CliRunner,
    astrobase_server: Generator,
) -> None:
    result = astrobase_cli_runner.invoke(
        app,
        [
            "cluster",
            "aks",
            "create",
            "--resource-group-name",
            "my-rg",
            "-f",
            f"{TEST_ASSET_DIR}/simple-aks.yaml",
        ],
    )
    assert result.exit_code == 0


@mock.patch(
    "requests.delete",
    return_value=mock.Mock(status_code=200, json=lambda: {"message": "Success!"}),
)
def test_cluster_aks_delete(
    mock_azure_provider_delete: mock.MagicMock,
    astrobase_cli_runner: CliRunner,
    astrobase_server: Generator,
) -> None:
    result = astrobase_cli_runner.invoke(
        app,
        [
            "cluster",
            "aks",
            "delete",
            "--resource-group-name",
            "my-rg",
            "-f",
            f"{TEST_ASSET_DIR}/simple-aks.yaml",
        ],
    )
    assert result.exit_code == 0
