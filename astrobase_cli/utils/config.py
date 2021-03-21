import json
import os
from typing import Optional

from pydantic import BaseModel

ASTROBASE_HOST_PORT = os.getenv("ASTROBASE_HOST_PORT", "8787")


class AstrobaseProfile(BaseModel):
    server: str = f"http://localhost:{ASTROBASE_HOST_PORT}"
    gcp_creds: Optional[str]
    aws_creds: Optional[str]
    aws_profile_name: Optional[str]


class AstrobaseConfig:
    ASTROBASE_PROFILE = "ASTROBASE_PROFILE"
    ASTROBASE_HOME_DIR = ".astrobase"
    ASTROBASE_CONFIG_FILENAME = "config.json"
    ASTROBASE_CONFIG_FULLPATH = (
        f"{os.getenv('HOME')}/{ASTROBASE_HOME_DIR}/{ASTROBASE_CONFIG_FILENAME}"
    )

    def __init__(self):
        self.config = self.ASTROBASE_CONFIG_FULLPATH

        try:
            self._setup_config_dir()
            self._setup_config_file()
        except FileExistsError:
            pass

        self.config_dict = self._load_config_file()
        self.profile_name = os.getenv(self.ASTROBASE_PROFILE)
        self.current_profile = None

        if self.config_dict and self.profile_name in self.config_dict:
            self.current_profile = AstrobaseProfile(
                **self.config_dict[self.profile_name]
            )

    def _setup_config_dir(self) -> None:
        os.makedirs(os.path.dirname(self.config))

    def _setup_config_file(self) -> None:
        if not os.path.exists(self.config):
            with open(self.config, "w+") as f:
                f.write("{}")

    def _load_config_file(self) -> dict:
        with open(self.config) as f:
            return json.load(f)

    def write_config(self, data: dict) -> None:
        with open(self.config, "w+") as f:
            f.write(json.dumps(data))


class AstrobaseDockerConfig:
    DOCKER_GROUP = "astrobase"
    DOCKER_CONTAINER_NAME = "astrobase"
    AWS_PROFILE_ENV_KEY = "AWS_PROFILE"
    AWS_CREDS_CONTAINER = "/aws-credentials"
    AWS_SHARED_CREDS_FILE_ENV_KEY = "AWS_SHARED_CREDENTIALS_FILE"
    GOOGLE_CREDS_CONTAINER = "/google-credentials.json"
    GOOGLE_APPLICATION_CREDS_ENV_KEY = "GOOGLE_APPLICATION_CREDENTIALS"

    def __init__(
        self,
        container_version: str,
        astrobase_config: AstrobaseConfig,
        environment: dict = {},
        volumes: dict = {},
        auto_remove: bool = True,
        detach: bool = True,
        host_port: str = ASTROBASE_HOST_PORT,
    ):
        self.image = (
            f"{self.DOCKER_GROUP}/{self.DOCKER_CONTAINER_NAME}:{container_version}"
        )
        self.ports = {f"{host_port}/tcp": str(host_port)}
        self.auto_remove = auto_remove
        self.detach = detach
        self.name = f"astrobase-{astrobase_config.profile_name}"
        self.astrobase_config = astrobase_config
        self.volumes = volumes
        self.environment = environment

        self._configure_aws()
        self._configure_gcp()

    def _configure_gcp(self) -> None:
        host_gcp_creds = self.astrobase_config.current_profile.gcp_creds
        if host_gcp_creds:
            self.environment[
                self.GOOGLE_APPLICATION_CREDS_ENV_KEY
            ] = self.GOOGLE_CREDS_CONTAINER
            self.volumes[host_gcp_creds] = {
                "bind": self.GOOGLE_CREDS_CONTAINER,
                "mode": "ro",
            }

    def _configure_aws(self) -> None:
        host_aws_creds = self.astrobase_config.current_profile.aws_creds
        if host_aws_creds:
            self.volumes[host_aws_creds] = {
                "bind": self.AWS_CREDS_CONTAINER,
                "mode": "ro",
            }
        aws_profile_name = self.astrobase_config.current_profile.aws_profile_name
        if aws_profile_name:
            self.environment[
                self.AWS_SHARED_CREDS_FILE_ENV_KEY
            ] = self.AWS_CREDS_CONTAINER
            self.environment[self.AWS_PROFILE_ENV_KEY] = aws_profile_name
