import os
import sys
from contextlib import contextmanager

import typer
from kubernetes import client, config
from sh import kubectl


class KubernetesClient:
    @contextmanager
    def kube_api_client(self) -> None:
        config.load_kube_config()
        yield client.ApiClient()

    def apply_kubernetes_resources(self, kubernetes_resource_dir: str) -> dict:
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
