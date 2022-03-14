import json
import os

import typer
from pydantic import BaseModel, StrictStr

ASTROBASE_HOST_PORT = os.getenv("ASTROBASE_HOST_PORT", "8787")


class AstrobaseProfile(BaseModel):
    name: str
    host: StrictStr = "localhost"
    port: int = int(ASTROBASE_HOST_PORT)
    secure: bool = True

    def url(self) -> str:
        result = f"{self.host}:{self.port}"
        return f"https://{result}" if self.secure else f"http://{result}"


class AstrobaseCLIConfig:
    ASTROBASE_CONFIG_FILE = "ASTROBASE_CONFIG"
    ASTROBASE_PROFILE_NAME = "ASTROBASE_PROFILE_NAME"
    DEFAULT_ASTROBASE_CONFIG_FILE = f"{os.getenv('HOME')}/.astrobase/config.json"

    def __init__(self) -> None:
        self.config_file = os.getenv(
            self.ASTROBASE_CONFIG_FILE,
            self.DEFAULT_ASTROBASE_CONFIG_FILE,
        )
        self._setup_config_dir()
        self._setup_config_file()
        self.config = self._load_config_file()

    def _setup_config_dir(self) -> None:
        if not os.path.exists(self.config_file):
            dirname = os.path.dirname(self.config_file)
            os.makedirs(dirname, exist_ok=True)

    def _setup_config_file(self) -> None:
        if not os.path.exists(self.config_file):
            with open(self.config_file, "w+") as f:
                f.write("{}")

    def _load_config_file(self) -> dict:
        with open(self.config_file) as f:
            return json.load(f)

    def write_config(self, data: dict) -> None:
        with open(self.config_file, "w+") as f:
            f.write(json.dumps(data, indent=2))

    def current_profile(self) -> AstrobaseProfile:
        profile_name = os.getenv(self.ASTROBASE_PROFILE_NAME)
        if not profile_name or profile_name not in self.config:
            typer.echo(
                "ASTROBASE_PROFILE_NAME environment variable is not set properly.\n"
                "Please set it by running\n"
                "`export ASTROBASE_PROFILE_NAME=<your-profile-name>`\n"
                "View profile names with `astrobase profile get`."
            )
            raise typer.Exit(1)
        return AstrobaseProfile(**self.config.get(profile_name, {}))
