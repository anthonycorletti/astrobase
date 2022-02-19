from typing import Dict, List

from fastapi import APIRouter, Body
from google.cloud.container_v1.types import Cluster

from astrobase.providers.gcp import GCPProvider
from astrobase.types.gcp import (
    GKECluster,
    GKEClusterAPIFilter,
    GKEClusterOperationResponse,
)
from astrobase.types.providers import Provider

router = APIRouter(tags=[Provider.gcp], prefix="/gcp")
gcp_provider = GCPProvider()


@router.post(path="/cluster", response_model=GKEClusterOperationResponse)
async def _create_gke_cluster(
    cluster: GKECluster = Body(...),
) -> GKEClusterOperationResponse:
    result = await gcp_provider.create_cluster_async(
        project_id=cluster.project_id,
        cluster=Cluster(**GKEClusterAPIFilter(**cluster.dict()).dict()),
    )
    return GKEClusterOperationResponse(
        operation_type=str(result.operation_type.name),
        self_link=result.self_link,
        target_link=result.target_link,
    )


@router.get(path="/cluster", response_model=List)
async def _get_gke_clusters(project_id: str, location: str) -> List[Dict]:
    pass


@router.delete(path="/cluster", response_model=GKEClusterOperationResponse)
async def _delete_gke_cluster(
    cluster: GKECluster = Body(...),
) -> GKEClusterOperationResponse:
    result = await gcp_provider.delete_cluster_async(
        project_id=cluster.project_id,
        cluster=Cluster(**GKEClusterAPIFilter(**cluster.dict()).dict()),
    )
    return GKEClusterOperationResponse(
        operation_type=str(result.operation_type.name),
        self_link=result.self_link,
        target_link=result.target_link,
    )
