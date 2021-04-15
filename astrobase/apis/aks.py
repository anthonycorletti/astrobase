import os

from azure.identity import ClientSecretCredential
from azure.mgmt.containerservice import ContainerServiceClient

from astrobase.config.logger import logger
from astrobase.schemas.aks import AKSCreate


class AKSApi:
    AZURE_SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID", None)
    AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID", None)
    AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID", None)
    AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET", None)

    def __init__(self):
        try:
            credential = ClientSecretCredential(
                tenant_id=self.AZURE_TENANT_ID,
                client_id=self.AZURE_CLIENT_ID,
                client_secret=self.AZURE_CLIENT_SECRET,
            )
            container_client = ContainerServiceClient(
                credential=credential,
                subscription_id=self.AZURE_SUBSCRIPTION_ID,
            )
            self.container_client = container_client
        except Exception as e:
            logger.error(
                "Failed to create ContainerServiceClient for the api server. "
                "Make sure you've set the AZURE_SUBSCRIPTION_ID AZURE_TENANT_ID "
                "AZURE_CLIENT_ID AZURE_CLIENT_SECRET environment variables.\n"
                f"Full exception:\n{e}"
            )

    def create(self, resource_group_name: str, cluster_create: AKSCreate) -> dict:
        logger.info(f"data –– {cluster_create.dict()}")
        managed_cluster_create = (
            self.container_client.managed_clusters.begin_create_or_update(
                resource_group_name=resource_group_name,
                resource_name=cluster_create.name,
                parameters=cluster_create.dict(),
            )
        )
        return dict(managed_cluster_create)

    def get(self, location: str):
        pass

    def describe(self, location: str, cluster_name: str):
        pass

    def delete(self, location: str, cluster_name: str):
        pass
