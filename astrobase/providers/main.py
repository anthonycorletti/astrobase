import json
from typing import Dict

import requests
import typer

from astrobase.cli.config import AstrobaseCLIConfig


class AstrobaseClient:
    def __init__(self) -> None:
        ab_config = AstrobaseCLIConfig()
        self.url = ab_config.current_profile().url()

    def create_cluster(self, provider: str, cluster_spec: Dict) -> None:
        res = requests.post(f"{self.url}/{provider}/cluster", json=cluster_spec)
        typer.echo(json.dumps(res.json(), indent=2))

    def delete_cluster(self, provider: str, cluster_spec: Dict) -> None:
        res = requests.delete(f"{self.url}/{provider}/cluster", json=cluster_spec)
        typer.echo(json.dumps(res.json(), indent=2))
