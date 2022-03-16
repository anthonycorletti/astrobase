from typing import Generator
from unittest import mock

from typer.testing import CliRunner

from astrobasecloud.cli.main import app
from tests.mocks import MockJsonResponse


@mock.patch("requests.post", return_value=MockJsonResponse(response={"mock": "value"}))
def test_gcp_provider_setup(
    mock_request_post: mock.MagicMock,
    astrobase_cli_runner: CliRunner,
    astrobase_server: Generator,
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
