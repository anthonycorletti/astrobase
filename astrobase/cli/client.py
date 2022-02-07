import json
from typing import Dict

import requests
import typer

from astrobase.cli.config import AstrobaseConfig
from astrobase.utils.http import query_str


class AstrobaseClient:
    def __init__(self) -> None:
        ab_config = AstrobaseConfig()
        self.url = ab_config.current_profile.url()

    def create_cluster(self, provider: str, cluster_spec: Dict) -> None:
        res = requests.post(f"{self.url}/{provider}", json=cluster_spec)
        typer.echo(json.dumps(res.json(), indent=2))

    def delete_cluster(self, provider: str, cluster_spec: Dict) -> None:
        params = {
            "location": cluster_spec.get("location"),
            "project_id": cluster_spec.get("project_id"),
        }
        res = requests.delete(
            f"{self.url}/{provider}/{cluster_spec['name']}?{query_str(params)}",
            json=cluster_spec,
        )
        typer.echo(json.dumps(res.json(), indent=2))
