from typing import Dict, List

from azure.mgmt.containerservice.models import ManagedCluster
from fastapi import APIRouter, Body

from astrobase.providers.azure import AzureProvider
from astrobase.types.azure import AKSCreate
from astrobase.types.provider import ProviderName

router = APIRouter(tags=[ProviderName.azure], prefix="/azure")
azure_provider = AzureProvider()


@router.post("/aks")
def create_aks_cluster(cluster_create: AKSCreate = Body(...)) -> Dict:
    return azure_provider.create(
        resource_group_name=cluster_create.resource_group_name,
        cluster_create=cluster_create,
    )


@router.get("/aks")
def get_aks_clusters(resource_group_name: str) -> List[Dict]:
    return azure_provider.get(resource_group_name=resource_group_name)


@router.get("/aks/{cluster_name}")
def describe_aks_cluster(
    cluster_name: str,
    resource_group_name: str,
) -> ManagedCluster:
    return azure_provider.describe(
        resource_group_name=resource_group_name,
        cluster_name=cluster_name,
    )


@router.delete("/aks/{cluster_name}")
def delete_aks_cluster(cluster_name: str, resource_group_name: str) -> Dict:
    return azure_provider.begin_delete(
        resource_group_name=resource_group_name,
        cluster_name=cluster_name,
    )
