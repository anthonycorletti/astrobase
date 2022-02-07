from typer.testing import CliRunner

from astrobase import __version__
from astrobase.cli.main import app

runner = CliRunner()


def test_cli_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout
