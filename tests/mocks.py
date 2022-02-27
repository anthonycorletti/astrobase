from typing import List
from unittest.mock import MagicMock

from google.api_core.exceptions import GoogleAPICallError

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
        self_link: str = None,
        target_link: str = None,
    ) -> None:
        self.operation = operation
        self.self_link = self_link or "https://google.com"
        self.target_link = target_link or "https://google.com"


class MockGKECluster:
    def __init__(self, name: str = None) -> None:
        self.name = "my-test-cluster"


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
        return MockGKEClusterOperation(operation=MockGCPOperation(name="createcluster"))

    def list_clusters(request: MockGKEListClusterRequest) -> MockGKEListClusterResponse:
        return MockGKEListClusterResponse()

    def get_cluster(request: MockGKEGetClusterRequest) -> MockGKECluster:
        return MockGKECluster()

    def delete_cluster(
        request: MockGKEDeleteClusterRequest,
    ) -> MockGKEClusterOperation:
        return MockGKEClusterOperation(operation=MockGCPOperation(name="deletecluster"))


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


class MockAzureContainerClient:
    pass
