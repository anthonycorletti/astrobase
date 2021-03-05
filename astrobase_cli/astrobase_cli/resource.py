import os
from typing import Optional

import typer
from kubernetes import client, utils


class Resource:
    def __init__(
        self,
        kubernetes_host_address: Optional[str],
        kubernetes_ssl_ca_cert: Optional[str],
    ):
        if kubernetes_host_address is not None and kubernetes_ssl_ca_cert is not None:
            self.kubernetes_config = client.Configuration(host=kubernetes_host_address)
            self.kubernetes_config.verify_ssl = True
            self.kubernetes_config.ssl_ca_cert = kubernetes_ssl_ca_cert
            self.kubernetes_api_client = client.ApiClient(
                configuration=self.kubernetes_config
            )
        else:
            self.kubernetes_api_client = None

    def apply_kubernetes_resources(self, kubernetes_resource_dir: str) -> dict:
        if not self.kubernetes_api_client:
            typer.echo("no kubernetes api client provisioned")
            return {}
        resource_yaml_files = [
            f for f in os.listdir(kubernetes_resource_dir) if f.endswith(".yaml")
        ]
        for yaml_file in resource_yaml_files:
            utils.create_from_yaml(
                self.kubernetes_api_client, f"{kubernetes_resource_dir}/{yaml_file}"
            )
