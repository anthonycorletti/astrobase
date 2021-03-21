from astrobase_cli.clients.eks import EKSClient
from astrobase_cli.clients.gke import GKEClient
from schemas.cluster import Clusters
from schemas.resource import ResourceList
from schemas.workflow import Workflows


class Apply:
    def __init__(self):
        self.clients = {"eks": EKSClient(), "gke": GKEClient()}

    def apply_clusters(self, clusters: Clusters) -> None:
        for cluster in clusters:
            client = self.clients.get(cluster.get("provider"))
            client.create(cluster)

    def apply_resources(self, resources: ResourceList) -> None:
        for resource in resources:
            client = self.clients.get(resource.provider)
            kubernetes_resource_location = resource.resource_location
            cluster_name = resource.cluster_name
            cluster_location = resource.cluster_location
            client.apply_kubernetes_resources(
                kubernetes_resource_location=kubernetes_resource_location,
                cluster_name=cluster_name,
                cluster_location=cluster_location,
            )

    def apply_workflows(self, workflows: Workflows) -> None:
        pass
