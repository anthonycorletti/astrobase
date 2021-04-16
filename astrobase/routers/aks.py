from fastapi import APIRouter, Body

from astrobase.apis.aks import AKSApi
from astrobase.schemas.aks import AKSCreate
from tests.factories import ClusterFactory

cluster_examples = ClusterFactory()
aks_api = AKSApi()
router = APIRouter()
tags = ["cluster", "aks"]


@router.post("/aks", tags=tags)
def create_aks_cluster(
    cluster_create: AKSCreate = Body(..., example=cluster_examples.aks_example()),
):
    return aks_api.create(
        resource_group_name=cluster_create.resource_group_name,
        cluster_create=cluster_create,
    )


@router.get("/aks", tags=tags)
def get_aks_clusters(
    resource_group_name: str,
):
    return aks_api.get(resource_group_name=resource_group_name)


@router.get("/aks/{cluster_name}", tags=tags)
def describe_aks_cluster(
    cluster_name: str,
    resource_group_name: str,
):
    return aks_api.describe(
        resource_group_name=resource_group_name,
        cluster_name=cluster_name,
    )


@router.delete("/aks/{cluster_name}", tags=tags)
def delete_aks_cluster(
    cluster_name: str,
    resource_group_name: str,
):
    return aks_api.begin_delete(
        resource_group_name=resource_group_name,
        cluster_name=cluster_name,
    )
