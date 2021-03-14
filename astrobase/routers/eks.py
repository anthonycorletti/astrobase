from typing import List

from fastapi import APIRouter, Body

from astrobase.apis.eks import EKSApi
from astrobase.schemas.eks import EKSCreate
from tests.factories import ClusterFactory

router = APIRouter()
tags = ["cluster"]


@router.post("/eks", tags=tags)
def create_eks_cluster(
    cluster_create: EKSCreate = Body(..., example=ClusterFactory.eks_create_example),
):
    eks_api = EKSApi(region=cluster_create.region)
    return eks_api.create(cluster_create)


@router.get("/eks", tags=tags)
def get_eks_clusters(region: str):
    eks_api = EKSApi(region=region)
    return eks_api.get()


@router.get("/eks/{cluster_name}", tags=tags)
def describe_eks_cluster(cluster_name: str, region: str):
    eks_api = EKSApi(region=region)
    return eks_api.describe(cluster_name=cluster_name)


@router.delete("/eks/{cluster_name}", tags=tags)
def delete_eks_cluster(
    cluster_name: str,
    region: str,
    nodegroup_names: List[str] = Body(..., example=[]),
):
    eks_api = EKSApi(region=region)
    return eks_api.delete(
        cluster_name=cluster_name,
        nodegroup_names=nodegroup_names,
    )
