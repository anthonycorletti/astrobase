import os
import sys
from contextlib import contextmanager

import typer
from kubernetes import client, config
from sh import aws, gcloud, kubectl


class KubernetesClient:
    @contextmanager
    def kube_api_client(self) -> None:
        config.load_kube_config()
        yield client.ApiClient()

    def apply_eks_kubernetes_resources(
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

    def apply_gke_kubernetes_resources(
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
