from unittest import mock

from fastapi.testclient import TestClient

from tests.factories import ClusterFactory
from tests.mocks import MockAzureContainerClient

cluster_examples = ClusterFactory()


@mock.patch(
    "astrobase.providers.azure.AzureProvider.container_client",
    return_value=MockAzureContainerClient(),
)
def test_create_cluster(
    mock_azure_container_client: mock.MagicMock, client: TestClient
) -> None:
    assert False


@mock.patch(
    "astrobase.providers.azure.AzureProvider.container_client",
    return_value=MockAzureContainerClient(),
)
def test_get_clusters(
    mock_azure_container_client: mock.MagicMock, client: TestClient
) -> None:
    assert False


@mock.patch(
    "astrobase.providers.azure.AzureProvider.container_client",
    return_value=MockAzureContainerClient(),
)
def test_describe_cluster(
    mock_azure_container_client: mock.MagicMock, client: TestClient
) -> None:
    assert False


@mock.patch(
    "astrobase.providers.azure.AzureProvider.container_client",
    return_value=MockAzureContainerClient(),
)
def test_delete_clister(
    mock_azure_container_client: mock.MagicMock, client: TestClient
) -> None:
    assert False
