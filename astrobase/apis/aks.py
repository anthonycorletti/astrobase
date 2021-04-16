import os
from typing import List

from azure.core.exceptions import ResourceExistsError
from azure.identity import ClientSecretCredential
from azure.mgmt.containerservice import ContainerServiceClient
from fastapi import HTTPException

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
        try:
            managed_cluster_create = (
                self.container_client.managed_clusters.begin_create_or_update(
                    resource_group_name=resource_group_name,
                    resource_name=cluster_create.name,
                    parameters=cluster_create.dict(),
                )
            )
            return {
                "result": managed_cluster_create.result,
                "status": managed_cluster_create.status,
            }
        except ResourceExistsError as e:
            logger.error(f"Create AKS cluster failed with: {e.message}")
            raise HTTPException(detail=e.message, status_code=400)

    def get(self, resource_group_name: str) -> List[dict]:
        m = self.container_client.managed_clusters
        return [
            cluster.as_dict()
            for cluster in m.list_by_resource_group(
                resource_group_name=resource_group_name
            )
        ]

    def describe(self, resource_group_name: str, cluster_name: str) -> dict:
        return self.container_client.managed_clusters.get(
            resource_group_name=resource_group_name,
            resource_name=cluster_name,
        )

    def delete(self, resource_group_name: str, cluster_name: str):
        managed_cluster_delete = self.container_client.managed_clusters.begin_delete(
            resource_group_name=resource_group_name, resource_name=cluster_name
        )
        return {
            "result": managed_cluster_delete.result,
            "status": managed_cluster_delete.status,
        }
