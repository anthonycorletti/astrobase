from fastapi import HTTPException
from google.api_core.exceptions import GoogleAPICallError
from google.api_core.operation_async import AsyncOperation
from google.cloud.container_v1 import (
    ClusterManagerAsyncClient,
    CreateClusterRequest,
    DeleteClusterRequest,
    GetClusterRequest,
    ListClustersRequest,
    ListClustersResponse,
    Operation,
)
from google.cloud.container_v1.types import Cluster
from google.cloud.service_usage_v1.services.service_usage import ServiceUsageAsyncClient
from google.cloud.service_usage_v1.types.serviceusage import EnableServiceRequest

from astrobase.providers._provider import Provider
from astrobase.types.gcp import GCPServiceNames, GCPSetupSpec


class GCPProvider(Provider):
    def __init__(self) -> None:
        super().__init__()
        self.cluster_manager_async_client = ClusterManagerAsyncClient()
        self.service_usage_async_client = ServiceUsageAsyncClient()

    def _parent(self, project_id: str, location: str) -> str:
        return f"projects/{project_id}/locations/{location}"

    def _name(self, project_id: str, location: str, cluster_id: str) -> str:
        return (
            f"{self._parent(project_id=project_id, location=location)}"
            f"/clusters/{cluster_id}"
        )

    def _enable_project_request_name(self, project_id: str, service_name: str) -> str:
        return f"projects/{project_id}/services/{service_name}"

    async def _enable_service(
        self, setup_spec: GCPSetupSpec, service_name: GCPServiceNames
    ) -> AsyncOperation:
        enable_service_request = EnableServiceRequest(
            name=self._enable_project_request_name(
                project_id=setup_spec.project_id,
                service_name=service_name.value,
            )
        )
        try:
            response = await self.service_usage_async_client.enable_service(
                request=enable_service_request
            )
            return response
        except GoogleAPICallError as e:
            if e.code is None:
                e.code = 500
            raise HTTPException(status_code=e.code, detail=e.message)

    async def setup(self, setup_spec: GCPSetupSpec) -> AsyncOperation:
        response = await self._enable_service(
            setup_spec=setup_spec, service_name=GCPServiceNames.container
        )
        return response

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

    async def get(self, project_id: str, location: str) -> ListClustersResponse:
        parent = self._parent(project_id=project_id, location=location)
        request = ListClustersRequest(parent=parent)
        try:
            response = await self.cluster_manager_async_client.list_clusters(
                request=request
            )
            return response
        except GoogleAPICallError as e:
            if e.code is None:
                e.code = 500
            raise HTTPException(status_code=e.code, detail=e.message)

    async def describe(
        self, project_id: str, location: str, cluster_name: str
    ) -> Cluster:
        name = self._name(
            project_id=project_id, location=location, cluster_id=cluster_name
        )
        request = GetClusterRequest(name=name)
        try:
            response = await self.cluster_manager_async_client.get_cluster(
                request=request
            )
            return response
        except GoogleAPICallError as e:
            if e.code is None:
                e.code = 500
            raise HTTPException(status_code=e.code, detail=e.message)

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
