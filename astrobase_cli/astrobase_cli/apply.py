from typing import List

from astrobase_cli.clients.eks import EKSClient
from astrobase_cli.clients.gke import GKEClient


class Apply:
    def __init__(self):
        self.clients = {"eks": EKSClient(), "gke": GKEClient()}

    def apply_clusters(self, clusters: List[dict]) -> None:
        for cluster in clusters:
            client = self.clients.get(cluster.get("provider"))
            client.create(cluster)

    def apply_resources(self, resources: List) -> None:
        for resource in resources:
            client = self.clients.get(resource.get("provider"))
            kubernetes_resource_dir = resource.get("resource_dir")
            cluster_name = resource.get("cluster_name")
            cluster_location = resource.get("cluster_location")
            client.apply_kubernetes_resources(
                kubernetes_resource_dir=kubernetes_resource_dir,
                cluster_name=cluster_name,
                cluster_location=cluster_location,
            )

    def apply_workflows(self, workflows: List) -> None:
        pass
