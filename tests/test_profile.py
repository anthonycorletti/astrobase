import json
import os

from typer.testing import CliRunner

from astrobase.cli.config import AstrobaseCLIConfig
from astrobase.cli.main import app

runner = CliRunner()


def test_profile_create(astrobase_profile_name: str) -> None:
    result = runner.invoke(
        app,
        [
            "profile",
            "create",
            astrobase_profile_name,
            "--gcp-creds",
            "test-gcp",
            "--aws-creds",
            "test-aws",
            "--aws-profile-name",
            "test-aws",
        ],
    )
    assert result.exit_code == 0
    assert f"Created profile {astrobase_profile_name}" in result.stdout


def test_profile_get(astrobase_profile_name: str) -> None:
    result = runner.invoke(app, ["profile", "get"])
    assert result.exit_code == 0
    config = json.loads(result.stdout)
    assert astrobase_profile_name in config
    result = runner.invoke(app, ["profile", "get", "--name", astrobase_profile_name])
    assert result.exit_code == 0
    config = json.loads(result.stdout)
    assert "server" in config
    result = runner.invoke(app, ["profile", "get", "--name", "noname"])
    assert result.exit_code == 0
    assert "profile noname not found" in result.stdout


def test_profile_current(astrobase_profile_name: str) -> None:
    result = runner.invoke(app, ["profile", "current"])
    assert result.exit_code == 0
    profile = json.loads(result.stdout)
    assert profile.get("name") == astrobase_profile_name
    assert profile.get("server") == "http://localhost:8787"


def test_profile_delete(astrobase_profile_name: str) -> None:
    result = runner.invoke(app, ["profile", "delete", "--name", astrobase_profile_name])
    assert result.exit_code == 0
    assert f"Deleted {astrobase_profile_name} profile" in result.stdout
    result = runner.invoke(app, ["profile", "delete", "--name", astrobase_profile_name])
    assert result.exit_code == 0
    assert f"Profile {astrobase_profile_name} not found" in result.stdout


def test_profile_current_not_set(astrobase_profile_name: str) -> None:
    del os.environ[AstrobaseCLIConfig.ASTROBASE_PROFILE_NAME]
    result = runner.invoke(app, ["profile", "current"])
    assert result.exit_code == 1
    assert (
        "ASTROBASE_PROFILE_NAME environment variable is not set properly."
        in result.stdout
    )
