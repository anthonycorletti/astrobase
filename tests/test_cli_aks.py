from typer.testing import CliRunner

from astrobase.cli.main import app
from tests.factories import TEST_ASSET_DIR


def test_cluster_aks_create(astrobase_cli_runner: CliRunner) -> None:
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
