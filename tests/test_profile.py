import json
import os

from typer.testing import CliRunner

from astrobase.cli.config import AstrobaseCLIConfig
from astrobase.cli.main import app

runner = CliRunner()


def test_profile_create() -> None:
    test_profile_name = os.getenv(AstrobaseCLIConfig.ASTROBASE_PROFILE_NAME)
    result = runner.invoke(
        app,
        [
            "profile",
            "create",
            test_profile_name,
            "--gcp-creds",
            "test-gcp",
            "--aws-creds",
            "test-aws",
            "--aws-profile-name",
            "test-aws",
        ],
    )
    assert result.exit_code == 0
    assert f"Created profile {test_profile_name}" in result.stdout


def test_profile_get() -> None:
    test_profile_name = os.getenv(AstrobaseCLIConfig.ASTROBASE_PROFILE_NAME)
    result = runner.invoke(app, ["profile", "get"])
    assert result.exit_code == 0
    config = json.loads(result.stdout)
    assert test_profile_name in config
    result = runner.invoke(app, ["profile", "get", "--name", test_profile_name])
    assert result.exit_code == 0
    config = json.loads(result.stdout)
    assert "server" in config
    result = runner.invoke(app, ["profile", "get", "--name", "noname"])
    assert result.exit_code == 0
    assert "profile noname not found" in result.stdout


def test_profile_current() -> None:
    test_profile_name = os.getenv(AstrobaseCLIConfig.ASTROBASE_PROFILE_NAME)
    result = runner.invoke(app, ["profile", "current"])
    assert result.exit_code == 0
    profile = json.loads(result.stdout)
    assert profile.get("name") == test_profile_name
    assert profile.get("server") == "http://localhost:8787"


def test_profile_delete() -> None:
    test_profile_name = os.getenv(AstrobaseCLIConfig.ASTROBASE_PROFILE_NAME)
    result = runner.invoke(app, ["profile", "delete", "--name", test_profile_name])
    assert result.exit_code == 0
    assert f"Deleted {test_profile_name} profile" in result.stdout
    result = runner.invoke(app, ["profile", "delete", "--name", test_profile_name])
    assert result.exit_code == 0
    assert f"Profile {test_profile_name} not found" in result.stdout


def test_profile_current_not_set() -> None:
    del os.environ[AstrobaseCLIConfig.ASTROBASE_PROFILE_NAME]
    result = runner.invoke(app, ["profile", "current"])
    assert result.exit_code == 1
    assert (
        "ASTROBASE_PROFILE_NAME environment variable is not set properly."
        in result.stdout
    )
