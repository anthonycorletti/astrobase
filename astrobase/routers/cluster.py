from fastapi import APIRouter, Body

from astrobase.providers.google import GoogleProvider
from astrobase.schemas.cluster import GoogleClusterCreate, GoogleClusterUpdate
from tests.factories import ClusterFactory

google_provider = GoogleProvider()
router = APIRouter()
tags = ["cluster"]


@router.post("/google/cluster", tags=tags)
def google_create_cluster(
    cluster_create: GoogleClusterCreate = Body(
        ..., example=ClusterFactory.google_create_example
    ),
):
    return google_provider.create_cluster(cluster_create)


@router.get("/google/cluster", tags=tags)
def google_get_clusters(project_id: str, zone: str):
    return google_provider.get_clusters(project_id, zone)


@router.get("/google/cluster/{cluster_name}", tags=tags)
def google_describe_cluster(
    cluster_name: str,
    project_id: str,
    zone: str,
):
    return google_provider.describe_cluster(
        project_id=project_id, zone=zone, cluster_name=cluster_name
    )


@router.patch("/google/cluster/{cluster_name}", tags=tags)
def google_update_cluster(
    cluster_name: str,
    project_id: str,
    zone: str,
    cluster_update: GoogleClusterUpdate = Body(
        ..., example=ClusterFactory.google_update_example
    ),
):
    return google_provider.update_cluster(
        cluster_name=cluster_name,
        project_id=project_id,
        zone=zone,
        cluster_update=cluster_update,
    )


@router.delete("/google/cluster/{cluster_name}", tags=tags)
def google_delete_cluster(
    cluster_name: str,
    project_id: str,
    zone: str,
):
    return google_provider.delete_cluster(
        cluster_name=cluster_name,
        project_id=project_id,
        zone=zone,
    )
