from fastapi import APIRouter, Body

from astrobase.apis.eks import EKSApi
from astrobase.schemas.eks import EKSCreate
from tests.factories import ClusterFactory

eks_api = EKSApi()
router = APIRouter()
tags = ["cluster"]


@router.post("/eks", tags=tags)
def create_eks_cluster(
    cluster_create: EKSCreate = Body(..., example=ClusterFactory.eks_create_example),
):
    print("first here with clusteR_crate", cluster_create)
    return eks_api.create(cluster_create)


@router.get("/eks", tags=tags)
def get_eks_clusters():
    return eks_api.get()


@router.get("/eks/{cluster_name}", tags=tags)
def describe_eks_cluster(cluster_name: str):
    return eks_api.describe(cluster_name=cluster_name)


@router.delete("/eks/{cluster_name}", tags=tags)
def delete_eks_cluster(cluster_name: str):
    return eks_api.delete(cluster_name=cluster_name)
