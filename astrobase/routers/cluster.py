from typing import List

from fastapi import APIRouter, Body

from astrobase.providers.google import GoogleProvider
from astrobase.schemas.cluster import (
    GoogleCluster,
    GoogleClusterCreate,
    GoogleClusterUpdate,
)
from tests.factories import ClusterFactory

google_provider = GoogleProvider()
router = APIRouter()
tags = ["cluster"]


@router.post("/google/cluster", tags=tags, response_model=GoogleCluster)
def google_create_cluster(
    cluster_create: GoogleClusterCreate = Body(
        ..., example=ClusterFactory.google_example
    ),
):
    return google_provider.create_cluster(cluster_create)


@router.get("/google/cluster", tags=tags, response_model=List[GoogleCluster])
def google_get_clusters():
    pass


@router.get("/google/cluster/{cluster_name}", tags=tags, response_model=GoogleCluster)
def google_describe_cluster(cluster_name: str):
    pass


@router.patch("/google/cluster", tags=tags, response_model=GoogleCluster)
def google_update_cluster(cluster_name: str, cluster: GoogleClusterUpdate):
    pass


@router.delete("/google/cluster", tags=tags)
def google_delete_cluster(cluster_name: str):
    pass
