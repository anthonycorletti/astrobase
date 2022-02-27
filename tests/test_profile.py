import json
from typing import Generator

from typer.testing import CliRunner

from astrobase.cli.main import app

runner = CliRunner()


def test_profile_create_get_delete(astrobase_profile: Generator) -> None:
    result = runner.invoke(app, ["profile", "get", "test-profile"])
    assert result.exit_code == 0
    assert json.loads(result.stdout) == {
        "host": "localhost",
        "name": "test-profile",
        "port": 8787,
        "secure": True,
    }


def test_profile_get_not_found(astrobase_profile: Generator) -> None:
    result = runner.invoke(app, ["profile", "get", "noname"])
    assert result.exit_code == 0
    assert "Profile noname not found" in result.stdout


def test_profile_current(astrobase_profile: Generator) -> None:
    result = runner.invoke(app, ["profile", "current"])
    assert result.exit_code == 0
    assert json.loads(result.stdout) == {
        "host": "localhost",
        "name": "test-profile",
        "port": 8787,
        "secure": True,
    }


def test_profile_delete_not_found() -> None:
    result = runner.invoke(app, ["profile", "delete", "doesnotexist"])
    assert result.exit_code == 0
    assert "Profile doesnotexist not found" in result.stdout


def test_profile_current_not_set() -> None:
    result = runner.invoke(app, ["profile", "current"])
    assert result.exit_code == 1
    assert (
        "ASTROBASE_PROFILE_NAME environment variable is not set properly."
        in result.stdout
    )
