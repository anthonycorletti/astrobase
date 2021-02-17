from typing import List

from fastapi import APIRouter, Body

from astrobase.apis.cluster import ClusterAPI
from astrobase.schemas.cluster import Cluster, ClusterCreate, ClusterUpdate
from tests.factories import ClusterFactory

cluster_api = ClusterAPI()
router = APIRouter()
tags = ["cluster"]


@router.post("/cluster", tags=tags, response_model=Cluster)
def create_cluster(
    cluster_create: ClusterCreate = Body(..., example=ClusterFactory.google_example),
):
    return cluster_api.create_cluster(cluster_create)


@router.get("/cluster", tags=tags, response_model=List[Cluster])
def get_clusters():
    pass


@router.get("/cluster/{cluster_name}", tags=tags, response_model=Cluster)
def describe_cluster(cluster_name: str):
    pass


@router.patch("/cluster", tags=tags, response_model=Cluster)
def update_cluster(cluster_name: str, cluster: ClusterUpdate):
    pass


@router.delete("/cluster", tags=tags)
def delete_cluster(cluster_name: str):
    pass
