from typing import Dict, List
from unittest.mock import MagicMock

from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from google.api_core.exceptions import GoogleAPICallError

from astrobasecloud.types.azure import AgentPoolProfiles
from tests.factories import ClusterFactory

cluster_factory = ClusterFactory()


class MockGCPOperation:
    def __init__(self, name: str = None, done: str = None) -> None:
        self.name = name
        self.done = done


class MockGKECoreOperation:
    def __init__(self, operation: MockGCPOperation = None) -> None:
        self.operation = operation


class MockGKEClusterOperation:
    def __init__(
        self,
        operation: MockGCPOperation = None,
        name: str = None,
        self_link: str = None,
        target_link: str = None,
    ) -> None:
        self.name = name
        self.self_link = self_link or "https://google.com"
        self.target_link = target_link or "https://google.com"


class MockGKECluster:
    def __init__(self, name: str = None) -> None:
        self.name = "my-test-cluster"
        self._pb = None


class MockGKECreateClusterRequest:
    pass


class MockGCPEnableServiceRequest:
    pass


class MockGKEListClusterRequest:
    pass


class MockGKEGetClusterRequest:
    pass


class MockGKEDeleteClusterRequest:
    pass


class MockGKEListClusterResponse:
    def __init__(self, clusters: List[MockGKECluster] = None) -> None:
        self.clusters = [MockGKECluster()]


class MockGKEClusterManagerClient(MagicMock):
    def create_cluster(request: MockGKECreateClusterRequest) -> MockGKEClusterOperation:
        return MockGKEClusterOperation(
            operation=MockGCPOperation(name="createcluster"),
            name="createcluster",
        )

    def list_clusters(request: MockGKEListClusterRequest) -> MockGKEListClusterResponse:
        return MockGKEListClusterResponse()

    def get_cluster(request: MockGKEGetClusterRequest) -> MockGKECluster:
        return MockGKECluster()

    def delete_cluster(
        request: MockGKEDeleteClusterRequest,
    ) -> MockGKEClusterOperation:
        return MockGKEClusterOperation(
            operation=MockGCPOperation(name="deletecluster"), name="deletecluster"
        )


class MockGKEServiceUsageClient(MagicMock):
    def enable_service(request: MockGCPEnableServiceRequest) -> MockGKECoreOperation:
        return MockGKECoreOperation(
            operation=MockGCPOperation(name="enablingservice", done="true")
        )


class MockGKEClusterManagerFailClient(MagicMock):
    def create_cluster(request: MockGKECreateClusterRequest) -> MockGKEClusterOperation:
        raise GoogleAPICallError(message="Failed to create cluster.")

    def list_clusters(request: MockGKEListClusterRequest) -> MockGKEListClusterResponse:
        raise GoogleAPICallError(message="Failed to list clusters.")

    def get_cluster(request: MockGKEGetClusterRequest) -> MockGKECluster:
        raise GoogleAPICallError(message="Failed to get cluster.")

    def delete_cluster(
        request: MockGKEDeleteClusterRequest,
    ) -> MockGKEClusterOperation:
        raise GoogleAPICallError(message="Failed to delete cluster.")


class MockGKEServiceUsageFailClient(MagicMock):
    def enable_service(request: MockGCPEnableServiceRequest) -> MockGKECoreOperation:
        raise GoogleAPICallError(message="Failed to enable service.")


class MockManagedCluster:
    def __init__(
        self,
        name: str = "my_mock_managed_cluster",
        location: str = "eastus",
        dns_prefix: str = "test",
        resource_group_name: str = "test-rg",
        agent_pool_profiles: List[AgentPoolProfiles] = None,
    ) -> None:
        self.name = name
        self.location = location
        self.dns_prefix = dns_prefix
        self.resource_group_name = resource_group_name
        self.agent_pool_profiles = [AgentPoolProfiles(name="test", mode="User")]

    def as_dict(self) -> Dict:
        return {
            "name": self.name,
            "location": self.location,
            "dns_prefix": self.dns_prefix,
            "resource_group_name": self.resource_group_name,
            "agent_pool_profiles": self.agent_pool_profiles,
        }


class MockAzureManagedClustersClient(MagicMock):
    def begin_create_or_update(
        self, resource_group_name: str, resource_name: str, parameters: Dict
    ) -> None:
        pass

    def list_by_resource_group(
        self, resource_group_name: str
    ) -> List[MockManagedCluster]:
        return [MockManagedCluster(resource_group_name=resource_group_name)]

    def get(self, resource_group_name: str, resource_name: str) -> MockManagedCluster:
        return MockManagedCluster(
            resource_group_name=resource_group_name, name=resource_name
        )

    def begin_delete(self, resource_group_name: str, resource_name: str) -> None:
        pass


class MockAzureContainerClient(MagicMock):
    def __init__(self, managed_clusters: MockAzureManagedClustersClient = None) -> None:
        super().__init__()
        self.managed_clusters = MockAzureManagedClustersClient()


class MockFailAzureManagedClustersClient(MagicMock):
    def begin_create_or_update(
        self, resource_group_name: str, resource_name: str, parameters: Dict
    ) -> None:
        raise ResourceExistsError

    def list_by_resource_group(
        self, resource_group_name: str
    ) -> List[MockManagedCluster]:
        raise ResourceNotFoundError

    def get(self, resource_group_name: str, resource_name: str) -> MockManagedCluster:
        raise ResourceNotFoundError

    def begin_delete(self, resource_group_name: str, resource_name: str) -> None:
        raise ResourceNotFoundError


class MockFailAzureContainerClient(MagicMock):
    def __init__(
        self, managed_clusters: MockFailAzureManagedClustersClient = None
    ) -> None:
        super().__init__()
        self.managed_clusters = MockFailAzureManagedClustersClient()


class MockJsonResponse:
    def __init__(self, response: Dict) -> None:
        self.response = response

    def json(self) -> Dict:
        return self.response
