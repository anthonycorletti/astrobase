import json

from typer.testing import CliRunner

from astrobasecloud.cli.main import app


def test_profile_create_get_delete(astrobase_cli_runner: CliRunner) -> None:
    result = astrobase_cli_runner.invoke(app, ["profile", "get", "test-profile"])
    assert result.exit_code == 0
    assert json.loads(result.stdout) == {
        "host": "localhost",
        "name": "test-profile",
        "port": 8787,
        "secure": False,
    }


def test_profile_create_duplicate(astrobase_cli_runner: CliRunner) -> None:
    result = astrobase_cli_runner.invoke(app, ["profile", "create", "test-profile"])
    assert result.exit_code == 1
    assert (
        result.stdout.strip()
        == "Name test-profile already present in config. Please try another name!"
    )


def test_profile_get_not_found(astrobase_cli_runner: CliRunner) -> None:
    result = astrobase_cli_runner.invoke(app, ["profile", "get", "noname"])
    assert result.exit_code == 0
    assert "Profile noname not found" in result.stdout


def test_profile_get_name_not_specified(astrobase_cli_runner: CliRunner) -> None:
    result = astrobase_cli_runner.invoke(app, ["profile", "get"])
    assert result.exit_code == 0
    assert json.loads(result.stdout) == ["test-profile"]


def test_profile_current(astrobase_cli_runner: CliRunner) -> None:
    result = astrobase_cli_runner.invoke(app, ["profile", "current"])
    assert result.exit_code == 0
    assert json.loads(result.stdout) == {
        "host": "localhost",
        "name": "test-profile",
        "port": 8787,
        "secure": False,
    }


def test_profile_delete_not_found(astrobase_cli_runner: CliRunner) -> None:
    result = astrobase_cli_runner.invoke(app, ["profile", "delete", "doesnotexist"])
    assert result.exit_code == 0
    assert "Profile doesnotexist not found" in result.stdout


def test_profile_current_not_set() -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["profile", "current"])
    assert result.exit_code == 1
    assert (
        "ASTROBASE_PROFILE_NAME environment variable is not set properly."
        in result.stdout
    )
