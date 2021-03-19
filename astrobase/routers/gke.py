from fastapi import APIRouter, Body

from astrobase.apis.gke import GKEApi
from astrobase.schemas.gke import GKECreate
from tests.factories import ClusterFactory

cluster_examples = ClusterFactory()
gke_api = GKEApi()
router = APIRouter()
tags = ["cluster"]


@router.post("/gke", response_model=dict, tags=tags)
def create_gke_cluster(
    cluster_create: GKECreate = Body(..., example=cluster_examples.gke_example()),
):
    return gke_api.create(cluster_create)


@router.get("/gke", response_model=dict, tags=tags)
def get_gke_clusters(
    project_id: str,
    location: str,
):
    return gke_api.get(project_id, location)


@router.get("/gke/{cluster_name}", response_model=dict, tags=tags)
def describe_gke_cluster(
    cluster_name: str,
    project_id: str,
    location: str,
):
    return gke_api.describe(
        project_id=project_id,
        location=location,
        cluster_name=cluster_name,
    )


@router.delete("/gke/{cluster_name}", response_model=dict, tags=tags)
def delete_gke_cluster(
    cluster_name: str,
    project_id: str,
    location: str,
):
    return gke_api.delete(
        cluster_name=cluster_name,
        project_id=project_id,
        location=location,
    )
