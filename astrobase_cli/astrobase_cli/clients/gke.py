import os
import sys
from contextlib import contextmanager

import requests
import typer
from kubernetes import client, config
from sh import gcloud, kubectl

from utils.config import AstrobaseConfig
from utils.http import query_str

astrobase_config = AstrobaseConfig()


class GKEClient:
    def __init__(self):
        self.url = f"{astrobase_config.server}/gke"

    @contextmanager
    def kube_api_client(self) -> None:
        config.load_kube_config()
        yield client.ApiClient()

    def create(self, cluster: dict) -> None:
        requests.post(self.url, json=cluster)

    def destroy(self, cluster: dict) -> None:
        params = {
            "location": cluster.get("location"),
            "project_id": cluster.get("project_id"),
        }
        cluster_url = f"{self.url}/{cluster.get('name')}?{query_str(params)}"
        requests.delete(cluster_url)

    def apply_kubernetes_resources(
        self,
        kubernetes_resource_dir: str,
        cluster_name: str,
        cluster_location: str,
    ) -> dict:
        gcloud(
            "container",
            "clusters",
            "get-credentials",
            cluster_name,
            "--region",
            cluster_location,
        )
        with self.kube_api_client() as kube_api_client:
            if not kube_api_client:
                typer.echo("no kubernetes api client provisioned")
                return {}
            resource_yaml_files = [
                f for f in os.listdir(kubernetes_resource_dir) if f.endswith(".yaml")
            ]
            for yaml_file in resource_yaml_files:
                kubectl(
                    "apply",
                    "-f",
                    f"{kubernetes_resource_dir}/{yaml_file}",
                    _out=sys.stdout,
                )
