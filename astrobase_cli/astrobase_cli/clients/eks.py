import sys
from contextlib import contextmanager

import requests
import typer
from kubernetes import client, config
from sh import aws, kubectl

from utils.config import AstrobaseConfig
from utils.formatter import json_out

astrobase_config = AstrobaseConfig()


class EKSClient:
    def __init__(self):
        server = astrobase_config.current_profile.server
        self.url = f"{server}/eks"

    def get_kubeconfig_credentials(
        self, cluster_name: str, cluster_location: str
    ) -> None:
        aws(
            "eks",
            "--region",
            cluster_location,
            "update-kubeconfig",
            "--name",
            cluster_name,
        )

    @contextmanager
    def kube_api_client(self) -> None:
        config.load_kube_config()
        yield client.ApiClient()

    def create(self, cluster: dict) -> None:
        for nodegroup in cluster.get("nodegroups", []):
            nodegroup["clusterName"] = cluster.get("name")
            nodegroup["subnets"] = cluster.get("resourcesVpcConfig", {}).get(
                "subnetIds", []
            )
        res = requests.post(self.url, json=cluster)
        typer.echo(json_out(res.json()))

    def destroy(self, cluster: dict) -> None:
        cluster_url = f"{self.url}/{cluster.get('name')}"
        nodegroup_names = [ng.get("nodegroupName") for ng in cluster.get("nodegroups")]
        res = requests.delete(
            f"{cluster_url}?region={cluster.get('region')}", json=nodegroup_names
        )
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
