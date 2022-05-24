from typing import List

from fastapi import APIRouter, Body
from google.cloud.container_v1.types import Cluster

from astrobasecloud.providers.gcp import gcp_provider
from astrobasecloud.types.gcp import (
    GCPProjectCreateOperationResponse,
    GCPSetupSpec,
    GKECluster,
    GKEClusterApiFilter,
    GKEClusterOperationResponse,
    GKEClusterRead,
)
from astrobasecloud.types.provider import ProviderName

router = APIRouter(tags=[ProviderName.gcp], prefix="/gcp")


@router.post(path="/setup", response_model=GCPProjectCreateOperationResponse)
def _setup_gcp(
    setup_spec: GCPSetupSpec = Body(...),
) -> GCPProjectCreateOperationResponse:
    response = gcp_provider.setup(setup_spec=setup_spec)
    return GCPProjectCreateOperationResponse(
        done=response.operation.done,
        name=response.operation.name,
    )


@router.post(path="/cluster", response_model=GKEClusterOperationResponse)
def _create_gke_cluster(
    cluster: GKECluster = Body(...),
) -> GKEClusterOperationResponse:
    result = gcp_provider.create(
        project_id=cluster.project_id,
        cluster=Cluster(**GKEClusterApiFilter(**cluster.dict()).dict()),
    )
    return GKEClusterOperationResponse(
        operation=str(result.name),
        self_link=result.self_link,
        target_link=result.target_link,
    )


@router.get(path="/cluster", response_model=List[GKEClusterRead])
def _get_gke_cluster(project_id: str, location: str) -> List[GKEClusterRead]:
    result = gcp_provider.get(project_id=project_id, location=location)
    data = [
        GKEClusterRead(
            name=cluster.name,
            location=location,
            project_id=project_id,
        )
        for cluster in result.clusters
    ]
    return data


@router.get(path="/cluster/{cluster_name}", response_model=GKEClusterApiFilter)
def _describe_gke_cluster(
    project_id: str, location: str, cluster_name: str
) -> GKEClusterApiFilter:
    return gcp_provider.describe(
        project_id=project_id, location=location, cluster_name=cluster_name
    )


@router.delete(path="/cluster", response_model=GKEClusterOperationResponse)
def _delete_gke_cluster(
    cluster: GKECluster = Body(...),
) -> GKEClusterOperationResponse:
    result = gcp_provider.delete(
        project_id=cluster.project_id,
        cluster=Cluster(**GKEClusterApiFilter(**cluster.dict()).dict()),
    )
    return GKEClusterOperationResponse(
        operation=str(result.name),
        self_link=result.self_link,
        target_link=result.target_link,
    )
