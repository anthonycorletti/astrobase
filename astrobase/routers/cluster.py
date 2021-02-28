from fastapi import APIRouter, Body

from astrobase.apis.gke import GKEApi
from astrobase.schemas.cluster import GKECreate, GKEUpdate
from tests.factories import ClusterFactory

gke_api = GKEApi()
router = APIRouter()
tags = ["cluster"]


@router.post("/gke", tags=tags)
def create_gke_cluster(
    cluster_create: GKECreate = Body(
        ..., example=ClusterFactory.google_kubernetes_create_example
    ),
):
    return gke_api.create_gke_cluster(cluster_create)


@router.get("/gke", tags=tags)
def get_gke_clusters(project_id: str, zone: str):
    return gke_api.get_gke_clusters(project_id, zone)


@router.get("/gke/{cluster_name}", tags=tags)
def describe_gke_cluster(
    cluster_name: str,
    project_id: str,
    zone: str,
):
    return gke_api.describe_gke_cluster(
        project_id=project_id, zone=zone, cluster_name=cluster_name
    )


@router.put("/gke/{cluster_name}", tags=tags)
def update_gke_cluster(
    cluster_name: str,
    project_id: str,
    zone: str,
    cluster_update: GKEUpdate = Body(
        ..., example=ClusterFactory.google_kubernetes_update_example
    ),
):
    return gke_api.update_gke_cluster(
        cluster_name=cluster_name,
        project_id=project_id,
        zone=zone,
        cluster_update=cluster_update,
    )


@router.delete("/gke/{cluster_name}", tags=tags)
def delete_gke_cluster(
    cluster_name: str,
    project_id: str,
    zone: str,
):
    return gke_api.delete_gke_cluster(
        cluster_name=cluster_name,
        project_id=project_id,
        zone=zone,
    )
