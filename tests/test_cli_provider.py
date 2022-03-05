from typing import Generator

from typer.testing import CliRunner

from astrobase.cli.main import app


def test_gcp_provider_setup(
    astrobase_cli_runner: CliRunner, astrobase_server: Generator
) -> None:
    result = astrobase_cli_runner.invoke(
        app,
        [
            "provider",
            "setup",
            "gcp",
            "--project-id",
            "my-test-project",
            "--service-name",
            "container.googleapis.com",
        ],
    )
    assert result.exit_code == 0
