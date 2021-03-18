import os
import sys
from contextlib import contextmanager

import requests
import typer
from kubernetes import client, config
from sh import aws, kubectl

from utils.config import AstrobaseConfig

astrobase_config = AstrobaseConfig()


class EKSClient:
    def __init__(self):
        server = astrobase_config.current_profile.server
        self.url = f"{server}/eks"

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
        typer.echo(res.json())

    def destroy(self, cluster: dict) -> None:
        cluster_url = f"{self.url}/{cluster.get('name')}"
        nodegroup_names = [ng.get("nodegroupName") for ng in cluster.get("nodegroups")]
        res = requests.delete(
            f"{cluster_url}?region={cluster.get('region')}", json=nodegroup_names
        )
        typer.echo(res.json())

    def apply_kubernetes_resources(
        self,
        kubernetes_resource_dir: str,
        cluster_name: str,
        cluster_location: str,
    ) -> dict:
        aws(
            "eks",
            "--region",
            cluster_location,
            "update-kubeconfig",
            "--name",
            cluster_name,
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
