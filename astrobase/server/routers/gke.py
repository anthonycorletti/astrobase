from typing import Dict

from fastapi import APIRouter, Body

from astrobase.providers.gke import GKEApi
from astrobase.schemas.gke import GKECreate

gke_api = GKEApi()
router = APIRouter()
tags = ["cluster", "gke"]


@router.post("/gke", tags=tags)
def create_gke_cluster(cluster_create: GKECreate = Body(...)) -> Dict:
    return gke_api.create(cluster_create)


@router.get("/gke", tags=tags)
def get_gke_clusters(project_id: str, location: str) -> Dict:
    return gke_api.get(project_id, location)


@router.get("/gke/{cluster_name}", tags=tags)
def describe_gke_cluster(cluster_name: str, project_id: str, location: str) -> Dict:
    return gke_api.describe(
        project_id=project_id,
        location=location,
        cluster_name=cluster_name,
    )


@router.delete("/gke/{cluster_name}", tags=tags)
def delete_gke_cluster(cluster_name: str, project_id: str, location: str) -> Dict:
    return gke_api.delete(
        cluster_name=cluster_name,
        project_id=project_id,
        location=location,
    )
