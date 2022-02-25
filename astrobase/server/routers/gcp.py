from typing import List

from fastapi import APIRouter, Body
from google.cloud.container_v1.types import Cluster

from astrobase.providers.gcp import GCPProvider
from astrobase.types.gcp import (
    GCPProjectCreateOperationResponse,
    GCPSetupSpec,
    GKECluster,
    GKEClusterOperationResponse,
    GKEClusterRead,
)
from astrobase.types.provider import ProviderName

router = APIRouter(tags=[ProviderName.gcp], prefix="/gcp")
gcp_provider = GCPProvider()


@router.post(path="/setup", response_model=GCPProjectCreateOperationResponse)
async def _setup_gcp(
    setup_spec: GCPSetupSpec = Body(...),
) -> GCPProjectCreateOperationResponse:
    provider = GCPProvider()
    response = await provider.setup(setup_spec=setup_spec)
    return GCPProjectCreateOperationResponse(
        done=response.operation.done,
        name=response.operation.name,
    )


@router.post(path="/cluster", response_model=GKEClusterOperationResponse)
async def _create_gke_cluster(
    project_id: str,
    cluster: GKECluster = Body(...),
) -> GKEClusterOperationResponse:
    result = await gcp_provider.create_cluster_async(
        project_id=project_id,
        cluster=Cluster(**GKECluster(**cluster.dict()).dict()),
    )
    return GKEClusterOperationResponse(
        operation_type=str(result.operation_type.name),
        self_link=result.self_link,
        target_link=result.target_link,
    )


@router.get(path="/cluster", response_model=List[GKEClusterRead])
async def _get_gke_cluster(project_id: str, location: str) -> List[GKEClusterRead]:
    result = await gcp_provider.get(project_id=project_id, location=location)
    data = [
        GKEClusterRead(
            name=cluster.name,
            location=location,
            project_id=project_id,
        )
        for cluster in result.clusters
    ]
    return data


@router.get(path="/cluster/{cluster_name}", response_model=List[GKEClusterRead])
async def _describe_gke_cluster(
    project_id: str, location: str, cluster_name: str
) -> GKEClusterRead:
    result = await gcp_provider.describe(
        project_id=project_id, location=location, cluster_name=cluster_name
    )
    return GKEClusterRead(
        name=result.name,
        location=location,
        project_id=project_id,
    )


@router.delete(path="/cluster", response_model=GKEClusterOperationResponse)
async def _delete_gke_cluster(
    project_id: str,
    cluster: GKECluster = Body(...),
) -> GKEClusterOperationResponse:
    result = await gcp_provider.delete_cluster_async(
        project_id=project_id,
        cluster=Cluster(**GKECluster(**cluster.dict()).dict()),
    )
    return GKEClusterOperationResponse(
        operation_type=str(result.operation_type.name),
        self_link=result.self_link,
        target_link=result.target_link,
    )
