from typing import List

from fastapi import APIRouter, Body

from astrobasecloud.providers.azure import azure_provider
from astrobasecloud.types.azure import (
    AKSCluster,
    AKSClusterFiltered,
    AKSClusterOperationResponse,
)
from astrobasecloud.types.provider import ProviderName

router = APIRouter(tags=[ProviderName.azure], prefix="/azure")


@router.post("/cluster", response_model=AKSClusterOperationResponse)
def create_aks_cluster(
    cluster_create: AKSCluster = Body(...),
) -> AKSClusterOperationResponse:
    return azure_provider.create(
        resource_group_name=cluster_create.resource_group_name,
        cluster_create=cluster_create,
    )


@router.get("/cluster", response_model=List[AKSClusterFiltered])
def get_aks_clusters(resource_group_name: str) -> List[AKSClusterFiltered]:
    return azure_provider.get(resource_group_name=resource_group_name)


@router.get("/cluster/{cluster_name}", response_model=AKSClusterFiltered)
def describe_aks_cluster(
    cluster_name: str, resource_group_name: str
) -> AKSClusterFiltered:
    return azure_provider.describe(
        resource_group_name=resource_group_name,
        cluster_name=cluster_name,
    )


@router.delete("/cluster/{cluster_name}", response_model=AKSClusterOperationResponse)
def delete_aks_cluster(
    cluster_name: str,
    resource_group_name: str,
) -> AKSClusterOperationResponse:
    return azure_provider.begin_delete(
        resource_group_name=resource_group_name,
        cluster_name=cluster_name,
    )
