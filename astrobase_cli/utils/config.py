import json
import os


class AstrobaseConfig:
    ASTROBASE_PROFILE = "ASTROBASE_PROFILE"

    def __init__(self):
        self.config = "/".join([os.getenv("HOME"), ".astrobase", "config.json"])

        try:
            self._setup_config_dir()
            self._setup_config_file()
        except FileExistsError:
            pass

        self.config_dict = self._load_config_file()
        self.profile_name = os.getenv(self.ASTROBASE_PROFILE)
        self.current_profile = None

        if self.config_dict and self.profile_name in self.config_dict:
            self.current_profile = self.config_dict[self.profile_name]

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
