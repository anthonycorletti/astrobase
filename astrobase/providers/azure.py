import os
from typing import List

from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from azure.core.polling import LROPoller
from azure.identity import ClientSecretCredential
from azure.mgmt.containerservice import ContainerServiceClient
from azure.mgmt.containerservice.models import ManagedCluster, ManagedClusterListResult
from fastapi import HTTPException

from astrobase.providers._provider import Provider
from astrobase.server.logger import logger
from astrobase.types.azure import AKSCluster, AKSClusterOperationResponse


class AzureProvider(Provider):
    AZURE_SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")
    AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
    AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
    AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")

    def __init__(self) -> None:
        pass

    def container_client(self) -> ContainerServiceClient:
        try:
            assert self.AZURE_SUBSCRIPTION_ID is not None
            assert self.AZURE_TENANT_ID is not None
            assert self.AZURE_CLIENT_ID is not None
            assert self.AZURE_CLIENT_SECRET is not None
            credential = ClientSecretCredential(
                tenant_id=self.AZURE_TENANT_ID,
                client_id=self.AZURE_CLIENT_ID,
                client_secret=self.AZURE_CLIENT_SECRET,
            )
            return ContainerServiceClient(
                credential=credential,
                subscription_id=self.AZURE_SUBSCRIPTION_ID,
            )
        except Exception as e:
            logger.error(
                "Failed to create ContainerServiceClient for the api server. "
                "Make sure you've set the AZURE_SUBSCRIPTION_ID AZURE_TENANT_ID "
                "AZURE_CLIENT_ID AZURE_CLIENT_SECRET environment variables.\n"
                f"Full exception:\n{e}"
            )

    def create(
        self, resource_group_name: str, cluster_create: AKSCluster
    ) -> AKSClusterOperationResponse:
        try:
            self.make_begin_create_or_update_request(
                resource_group_name=resource_group_name, cluster_create=cluster_create
            )
            return AKSClusterOperationResponse(
                message=f"AKS create request submitted for {cluster_create.name}"
            )
        except ResourceExistsError as e:
            logger.error(f"Create AKS cluster failed with: {e.message}")
            raise HTTPException(detail=e.message, status_code=400)

    def make_begin_create_or_update_request(
        self, resource_group_name: str, cluster_create: AKSCluster
    ) -> LROPoller[ManagedCluster]:
        return self.container_client().managed_clusters.begin_create_or_update(
            resource_group_name=resource_group_name,
            resource_name=cluster_create.name,
            parameters=cluster_create.dict(),
        )

    def get(self, resource_group_name: str) -> List[AKSCluster]:
        try:
            return [
                AKSCluster(**cluster.as_dict())
                for cluster in self.make_get_request(
                    resource_group_name=resource_group_name
                )
            ]
        except ResourceNotFoundError as e:
            logger.error(
                "Get AKS clusters failed for resource "
                f"group {resource_group_name} with: {e.message}"
            )
            raise HTTPException(detail=e.message, status_code=400)

    def make_get_request(self, resource_group_name: str) -> ManagedClusterListResult:
        return self.container_client().managed_clusters.list_by_resource_group(
            resource_group_name=resource_group_name
        )

    def describe(self, resource_group_name: str, cluster_name: str) -> AKSCluster:
        try:
            return self.container_client().managed_clusters.get(
                resource_group_name=resource_group_name,
                resource_name=cluster_name,
            )
        except ResourceNotFoundError as e:
            logger.error(
                f"Get AKS cluster {cluster_name} failed for resource "
                f"group {resource_group_name} with: {e.message}"
            )
            raise HTTPException(detail=e.message, status_code=400)

    def begin_delete(
        self, resource_group_name: str, cluster_name: str
    ) -> AKSClusterOperationResponse:
        try:
            self.make_begin_delete_request(
                resource_group_name=resource_group_name, cluster_name=cluster_name
            )
            return AKSClusterOperationResponse(
                message=f"AKS delete request submitted for {cluster_name}"
            )
        except ResourceNotFoundError as e:
            logger.error(
                f"Delete AKS cluster {cluster_name} failed for resource "
                f"group {resource_group_name} with: {e.message}"
            )
            raise HTTPException(detail=e.message, status_code=400)

    def make_begin_delete_request(
        self, resource_group_name: str, cluster_name: str
    ) -> LROPoller:
        return self.container_client().managed_clusters.begin_delete(
            resource_group_name=resource_group_name, resource_name=cluster_name
        )
