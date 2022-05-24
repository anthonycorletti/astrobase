from fastapi import HTTPException
from google.api_core.exceptions import GoogleAPICallError
from google.api_core.operation import Operation as CoreOperation
from google.cloud.container_v1 import (
    ClusterManagerClient,
    CreateClusterRequest,
    DeleteClusterRequest,
    GetClusterRequest,
    ListClustersRequest,
    ListClustersResponse,
)
from google.cloud.container_v1.types import Cluster, Operation
from google.cloud.service_usage_v1.services.service_usage import ServiceUsageClient
from google.cloud.service_usage_v1.types.serviceusage import EnableServiceRequest
from google.protobuf.json_format import MessageToDict  # type: ignore

from astrobasecloud.providers._provider import Provider
from astrobasecloud.types.gcp import GCPSetupSpec, GKEClusterApiFilter


class GCPProvider(Provider):
    def __init__(self) -> None:
        super().__init__()

    def _cluster_manager_client(self) -> ClusterManagerClient:
        return ClusterManagerClient()  # pragma: no cover

    def _service_usage_client(self) -> ServiceUsageClient:
        return ServiceUsageClient()  # pragma: no cover

    def _parent(self, project_id: str, location: str) -> str:
        return f"projects/{project_id}/locations/{location}"

    def _name(self, project_id: str, location: str, cluster_id: str) -> str:
        return (
            f"{self._parent(project_id=project_id, location=location)}"
            f"/clusters/{cluster_id}"
        )

    def _enable_project_request_name(self, project_id: str, service_name: str) -> str:
        return f"projects/{project_id}/services/{service_name}"

    def _enable_service(
        self,
        setup_spec: GCPSetupSpec,
    ) -> CoreOperation:
        enable_service_request = EnableServiceRequest(
            name=self._enable_project_request_name(
                project_id=setup_spec.project_id,
                service_name=setup_spec.service_name.value,
            )
        )
        try:
            response = self._service_usage_client().enable_service(
                request=enable_service_request
            )
            return response
        except GoogleAPICallError as e:
            if e.code is None:
                e.code = 500
            raise HTTPException(status_code=e.code, detail=e.message)

    def setup(self, setup_spec: GCPSetupSpec) -> CoreOperation:
        response = self._enable_service(setup_spec=setup_spec)
        return response

    def create(self, project_id: str, cluster: Cluster) -> Operation:
        parent = self._parent(project_id=project_id, location=cluster.location)
        request = CreateClusterRequest(parent=parent, cluster=cluster)
        try:
            response = self._cluster_manager_client().create_cluster(request=request)
            return response
        except GoogleAPICallError as e:
            if e.code is None:
                e.code = 500
            raise HTTPException(status_code=e.code, detail=e.message)

    def get(self, project_id: str, location: str) -> ListClustersResponse:
        parent = self._parent(project_id=project_id, location=location)
        request = ListClustersRequest(parent=parent)
        try:
            response = self._cluster_manager_client().list_clusters(request=request)
            return response
        except GoogleAPICallError as e:
            if e.code is None:
                e.code = 500
            raise HTTPException(status_code=e.code, detail=e.message)

    def describe(
        self, project_id: str, location: str, cluster_name: str
    ) -> GKEClusterApiFilter:
        name = self._name(
            project_id=project_id, location=location, cluster_id=cluster_name
        )
        request = GetClusterRequest(name=name)
        try:
            response = self._cluster_manager_client().get_cluster(request=request)
            data = MessageToDict(message=response._pb, preserving_proto_field_name=True)
            return GKEClusterApiFilter(**data)
        except GoogleAPICallError as e:
            if e.code is None:
                e.code = 500
            raise HTTPException(status_code=e.code, detail=e.message)

    def delete(self, project_id: str, cluster: Cluster) -> Operation:
        parent = self._parent(project_id=project_id, location=cluster.location)
        request = DeleteClusterRequest(name=f"{parent}/clusters/{cluster.name}")
        try:
            response = self._cluster_manager_client().delete_cluster(request=request)
            return response
        except GoogleAPICallError as e:
            if e.code is None:
                e.code = 500
            raise HTTPException(status_code=e.code, detail=e.message)


gcp_provider = GCPProvider()
