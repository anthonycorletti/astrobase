from typing import List

from azure.mgmt.containerservice.models import ManagedCluster
from fastapi import APIRouter, Body

from astrobase.providers.azure import AzureProvider
from astrobase.types.azure import AKSCluster, AKSClusterOperationResponse
from astrobase.types.provider import ProviderName

router = APIRouter(tags=[ProviderName.azure], prefix="/azure")
azure_provider = AzureProvider()


@router.post("/cluster", response_model=AKSClusterOperationResponse)
def create_aks_cluster(
    cluster_create: AKSCluster = Body(...),
) -> AKSClusterOperationResponse:
    return azure_provider.create(
        resource_group_name=cluster_create.resource_group_name,
        cluster_create=cluster_create,
    )


@router.get("/cluster", response_model=List[AKSCluster])
def get_aks_clusters(resource_group_name: str) -> List[AKSCluster]:
    return azure_provider.get(resource_group_name=resource_group_name)


@router.get("/cluster/{cluster_name}", response_model=AKSCluster)
def describe_aks_cluster(cluster_name: str, resource_group_name: str) -> ManagedCluster:
    return azure_provider.describe(
        resource_group_name=resource_group_name,
        cluster_name=cluster_name,
    )


@router.delete("/cluster", response_model=AKSClusterOperationResponse)
def delete_aks_cluster(
    cluster_create: AKSCluster = Body(...),
) -> AKSClusterOperationResponse:
    return azure_provider.begin_delete(
        resource_group_name=cluster_create.resource_group_name,
        cluster_name=cluster_create.name,
    )
