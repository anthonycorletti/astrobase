from astrobase_cli.clients.eks import EKSClient
from astrobase_cli.clients.gke import GKEClient
from schemas.cluster import Clusters
from schemas.resource import ResourceList
from schemas.workflow import Workflows


class Destroy:
    def __init__(self):
        self.clients = {"eks": EKSClient(), "gke": GKEClient()}

    def destroy_clusters(self, clusters: Clusters) -> None:
        for cluster in clusters:
            client = self.clients.get(cluster.provider)
            client.destroy(cluster)

    def destroy_resources(self, resources: ResourceList) -> None:
        for resource in resources:
            client = self.clients.get(resource.provider)
            kubernetes_resource_location = resource.resource_location
            cluster_name = resource.cluster_name
            cluster_location = resource.cluster_location
            client.destroy_kubernetes_resources(
                kubernetes_resource_location=kubernetes_resource_location,
                cluster_name=cluster_name,
                cluster_location=cluster_location,
            )

    def destroy_workflows(self, workflows: Workflows) -> None:
        pass
