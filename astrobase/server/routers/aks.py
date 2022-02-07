from typing import Dict, List

from azure.mgmt.containerservice.models import ManagedCluster
from fastapi import APIRouter, Body

from astrobase.providers.aks import AKSApi
from astrobase.schemas.aks import AKSCreate

aks_api = AKSApi()
router = APIRouter()
tags = ["cluster", "aks"]


@router.post("/aks", tags=tags)
def create_aks_cluster(cluster_create: AKSCreate = Body(...)) -> Dict:
    return aks_api.create(
        resource_group_name=cluster_create.resource_group_name,
        cluster_create=cluster_create,
    )


@router.get("/aks", tags=tags)
def get_aks_clusters(resource_group_name: str) -> List[Dict]:
    return aks_api.get(resource_group_name=resource_group_name)


@router.get("/aks/{cluster_name}", tags=tags)
def describe_aks_cluster(cluster_name: str, resource_group_name: str) -> ManagedCluster:
    return aks_api.describe(
        resource_group_name=resource_group_name,
        cluster_name=cluster_name,
    )


@router.delete("/aks/{cluster_name}", tags=tags)
def delete_aks_cluster(cluster_name: str, resource_group_name: str) -> Dict:
    return aks_api.begin_delete(
        resource_group_name=resource_group_name,
        cluster_name=cluster_name,
    )
