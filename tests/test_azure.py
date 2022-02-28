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
    response = client.post(
        "/azure/cluster", json=cluster_examples.aks_example_complete_spec()
    )
    assert response.status_code == 200
    assert (
        response.json().get("message")
        == "AKS create request submitted for my-aks-cluster"
    )


@mock.patch(
    "astrobase.providers.azure.AzureProvider.container_client",
    return_value=MockAzureContainerClient(),
)
def test_get_clusters(
    mock_azure_container_client: mock.MagicMock, client: TestClient
) -> None:
    response = client.get("/azure/cluster?resource_group_name=test-rg")
    assert response.status_code == 200
    assert response.json()[0]["name"] == "my_mock_managed_cluster"


@mock.patch(
    "astrobase.providers.azure.AzureProvider.container_client",
    return_value=MockAzureContainerClient(),
)
def test_describe_cluster(
    mock_azure_container_client: mock.MagicMock, client: TestClient
) -> None:
    response = client.get("/azure/cluster/my-cluster?resource_group_name=test-rg")
    assert response.status_code == 200
    assert response.json()["name"] == "my-cluster"


@mock.patch(
    "astrobase.providers.azure.AzureProvider.container_client",
    return_value=MockAzureContainerClient(),
)
def test_delete_clister(
    mock_azure_container_client: mock.MagicMock, client: TestClient
) -> None:
    response = client.delete(
        "/azure/cluster", json=cluster_examples.aks_example_complete_spec()
    )
    assert response.status_code == 200
    assert (
        response.json().get("message")
        == "AKS delete request submitted for my-aks-cluster"
    )
