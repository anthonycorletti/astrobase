from fastapi import APIRouter, Body

from astrobase.apis.gke import GKEApi
from astrobase.schemas.gke import GKECreate, GKEResourceCreate
from tests.factories import ClusterFactory, ResourceFactory

gke_api = GKEApi()
router = APIRouter()
tags = ["cluster"]


@router.post("/gke", tags=tags)
def create_gke_cluster(
    cluster_create: GKECreate = Body(..., example=ClusterFactory.gke_create_example),
):
    return gke_api.create(cluster_create)


@router.get("/gke", tags=tags)
def get_gke_clusters(
    project_id: str = "astrobase-284118",
    location: str = "us-central1",
):
    return gke_api.get(project_id, location)


@router.get("/gke/{cluster_name}", tags=tags)
def describe_gke_cluster(
    cluster_name: str,
    project_id: str = "astrobase-284118",
    location: str = "us-central1",
):
    return gke_api.describe(
        project_id=project_id,
        location=location,
        cluster_name=cluster_name,
    )


@router.delete("/gke/{cluster_name}", tags=tags)
def delete_gke_cluster(
    cluster_name: str,
    project_id: str = "astrobase-284118",
    location: str = "us-central1",
):
    return gke_api.delete(
        cluster_name=cluster_name,
        project_id=project_id,
        location=location,
    )


@router.post("/gke/{cluster_name}/resource", tags=tags)
def create_gke_resource(
    cluster_name: str,
    project_id: str = "astrobase-284118",
    location: str = "us-central1",
    gke_resource_create: GKEResourceCreate = Body(
        ..., example=ResourceFactory.gke_resource_example
    ),
):
    return gke_api.create_resource(
        cluster_name, project_id, location, gke_resource_create
    )


@router.get("/gke/{cluster_name}/resource", tags=tags)
def get_gke_resources(cluster_name: str):
    return gke_api.get_resources(cluster_name)


@router.get("/gke/{cluster_name}/resource/{resource_name}", tags=tags)
def get_gke_resource(
    resource_name: str,
    cluster_name: str,
    project_id: str = "astrobase-284118",
    location: str = "us-central1",
):
    return gke_api.get_resource(cluster_name, resource_name, project_id, location)


@router.delete("/gke/{cluster_name}/resource/{resource_name}", tags=tags)
def delete_gke_resource(
    resource_name: str,
    cluster_name: str,
    project_id: str = "astrobase-284118",
    location: str = "us-central1",
):
    return gke_api.delete_resource(cluster_name, resource_name, project_id, location)
