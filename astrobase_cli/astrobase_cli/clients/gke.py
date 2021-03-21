import sys
from contextlib import contextmanager

import requests
import typer
from kubernetes import client, config
from sh import gcloud, kubectl

from utils.config import AstrobaseConfig
from utils.formatter import json_out
from utils.http import query_str

astrobase_config = AstrobaseConfig()


class GKEClient:
    def __init__(self):
        server = astrobase_config.current_profile.server
        self.url = f"{server}/gke"

    def get_kubeconfig_credentials(
        self, cluster_name: str, cluster_location: str
    ) -> None:
        gcloud(
            "container",
            "clusters",
            "get-credentials",
            cluster_name,
            "--region",
            cluster_location,
        )

    @contextmanager
    def kube_api_client(self) -> None:
        config.load_kube_config()
        yield client.ApiClient()

    def create(self, cluster: dict) -> None:
        res = requests.post(self.url, json=cluster)
        typer.echo(json_out(res.json()))

    def destroy(self, cluster: dict) -> None:
        params = {
            "location": cluster.get("location"),
            "project_id": cluster.get("project_id"),
        }
        cluster_url = f"{self.url}/{cluster.get('name')}?{query_str(params)}"
        res = requests.delete(cluster_url)
        typer.echo(json_out(res.json()))

    def apply_kubernetes_resources(
        self,
        kubernetes_resource_location: str,
        cluster_name: str,
        cluster_location: str,
    ) -> None:
        self.get_kubeconfig_credentials(cluster_name, cluster_location)
        typer.echo(f"applying resources to {cluster_name}@{cluster_location}")
        with self.kube_api_client() as kube_api_client:
            if not kube_api_client:
                typer.echo("no kubernetes api client provisioned")
                raise typer.Exit(1)
            kubectl("apply", "-f", f"{kubernetes_resource_location}", _out=sys.stdout)

    def destroy_kubernetes_resources(
        self,
        kubernetes_resource_location: str,
        cluster_name: str,
        cluster_location: str,
    ) -> None:
        self.get_kubeconfig_credentials(cluster_name, cluster_location)
        typer.echo(f"destroying resources in {cluster_name}@{cluster_location}")
        with self.kube_api_client() as kube_api_client:
            if not kube_api_client:
                typer.echo("no kubernetes api client provisioned")
                raise typer.Exit(1)
            kubectl("delete", "-f", f"{kubernetes_resource_location}", _out=sys.stdout)
