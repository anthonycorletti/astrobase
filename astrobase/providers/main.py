import json
from typing import Dict

import requests
import typer

from astrobase.cli.config import AstrobaseCLIConfig
from astrobase.types.provider import ProviderName


class AstrobaseGCPClient:
    def __init__(self) -> None:
        ab_config = AstrobaseCLIConfig()
        self.url = ab_config.current_profile().url()

    def _echo_response(self, data: object) -> None:
        typer.echo(json.dumps(data, indent=2))

    def create_cluster(self, cluster_spec: Dict) -> None:
        res = requests.post(
            f"{self.url}/{ProviderName.gcp}/cluster",
            json=cluster_spec,
        )
        self._echo_response(res.json())

    def delete_cluster(self, cluster_spec: Dict) -> None:
        res = requests.delete(
            f"{self.url}/{ProviderName.gcp}/cluster",
            json=cluster_spec,
        )
        self._echo_response(res.json())

    def setup_provider(self, setup_spec: Dict) -> None:
        res = requests.post(
            f"{self.url}/{ProviderName.gcp}/setup",
            json=setup_spec,
        )
        self._echo_response(res.json())


class AstrobaseAWSClient:
    def __init__(self) -> None:
        ab_config = AstrobaseCLIConfig()
        self.url = ab_config.current_profile().url()

    def _echo_response(self, data: object) -> None:
        typer.echo(json.dumps(data, indent=2))

    def create_cluster(self, cluster_spec: Dict) -> None:
        res = requests.post(
            f"{self.url}/{ProviderName.aws}/cluster",
            json=cluster_spec,
        )
        self._echo_response(res.json())

    def delete_cluster(self, cluster_spec: Dict) -> None:
        res = requests.delete(
            f"{self.url}/{ProviderName.aws}/cluster",
            json=cluster_spec,
        )
        self._echo_response(res.json())

    def setup_provider(self, setup_spec: Dict) -> None:
        res = requests.post(
            f"{self.url}/{ProviderName.aws}/setup",
            json=setup_spec,
        )
        self._echo_response(res.json())


class AstrobaseAzureClient:
    def __init__(self) -> None:
        ab_config = AstrobaseCLIConfig()
        self.url = ab_config.current_profile().url()

    def _echo_response(self, data: object) -> None:
        typer.echo(json.dumps(data, indent=2))

    def create_cluster(self, cluster_spec: Dict) -> None:
        res = requests.post(
            f"{self.url}/{ProviderName.azure}/cluster",
            json=cluster_spec,
        )
        self._echo_response(res.json())

    def delete_cluster(self, cluster_spec: Dict) -> None:
        res = requests.delete(
            f"{self.url}/{ProviderName.azure}/cluster",
            json=cluster_spec,
        )
        self._echo_response(res.json())

    def setup_provider(self, setup_spec: Dict) -> None:
        res = requests.post(
            f"{self.url}/{ProviderName.azure}/setup",
            json=setup_spec,
        )
        self._echo_response(res.json())
