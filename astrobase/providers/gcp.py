from typing import Dict, List

from fastapi import HTTPException
from google.api_core.exceptions import GoogleAPICallError
from google.cloud.container_v1 import (
    ClusterManagerAsyncClient,
    CreateClusterRequest,
    DeleteClusterRequest,
    Operation,
)
from google.cloud.container_v1.types import Cluster


class GCPProvider:
    def __init__(self) -> None:
        self.cluster_manager_async_client = ClusterManagerAsyncClient()

    def _parent(self, project_id: str, location: str) -> str:
        return f"projects/{project_id}/locations/{location}"

    async def create_cluster_async(
        self, project_id: str, cluster: Cluster
    ) -> Operation:
        parent = self._parent(project_id=project_id, location=cluster.location)
        request = CreateClusterRequest(parent=parent, cluster=cluster)
        try:
            response = await self.cluster_manager_async_client.create_cluster(
                request=request
            )
            return response
        except GoogleAPICallError as e:
            if e.code is None:
                e.code = 500
            raise HTTPException(status_code=e.code, detail=e.message)

    def get(self, project_id: str, location: str) -> List[Dict]:
        pass

    async def delete_cluster_async(
        self, project_id: str, cluster: Cluster
    ) -> Operation:
        parent = self._parent(project_id=project_id, location=cluster.location)
        request = DeleteClusterRequest(name=f"{parent}/clusters/{cluster.name}")
        try:
            response = await self.cluster_manager_async_client.delete_cluster(
                request=request
            )
            return response
        except GoogleAPICallError as e:
            if e.code is None:
                e.code = 500
            raise HTTPException(status_code=e.code, detail=e.message)
