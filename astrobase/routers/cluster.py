from fastapi import APIRouter, Body

from astrobase.providers.google import GoogleProvider
from astrobase.schemas.cluster import (
    GoogleKubernetesClusterCreate,
    GoogleKubernetesClusterUpdate,
)
from tests.factories import ClusterFactory

google_provider = GoogleProvider()
router = APIRouter()
tags = ["cluster"]


@router.post("/google/kubernetes/cluster", tags=tags)
def google_create_kubernetes_cluster(
    cluster_create: GoogleKubernetesClusterCreate = Body(
        ..., example=ClusterFactory.google_kubernetes_create_example
    ),
):
    return google_provider.create_kubernetes_cluster(cluster_create)


@router.get("/google/kubernetes/cluster", tags=tags)
def google_get_clusters(project_id: str, zone: str):
    return google_provider.get_clusters(project_id, zone)


@router.get("/google/kubernetes/cluster/{cluster_name}", tags=tags)
def google_describe_kubernetes_cluster(
    cluster_name: str,
    project_id: str,
    zone: str,
):
    return google_provider.describe_kubernetes_cluster(
        project_id=project_id, zone=zone, cluster_name=cluster_name
    )


@router.patch("/google/kubernetes/cluster/{cluster_name}", tags=tags)
def google_update_kubernetes_cluster(
    cluster_name: str,
    project_id: str,
    zone: str,
    cluster_update: GoogleKubernetesClusterUpdate = Body(
        ..., example=ClusterFactory.google_kubernetes_update_example
    ),
):
    return google_provider.update_kubernetes_cluster(
        cluster_name=cluster_name,
        project_id=project_id,
        zone=zone,
        cluster_update=cluster_update,
    )


@router.delete("/google/kubernetes/cluster/{cluster_name}", tags=tags)
def google_delete_kubernetes_cluster(
    cluster_name: str,
    project_id: str,
    zone: str,
):
    return google_provider.delete_kubernetes_cluster(
        cluster_name=cluster_name,
        project_id=project_id,
        zone=zone,
    )
