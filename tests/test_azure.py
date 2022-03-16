import os
from unittest import mock

import pytest
from fastapi.exceptions import HTTPException
from fastapi.testclient import TestClient

from tests.factories import ClusterFactory
from tests.mocks import MockAzureContainerClient, MockFailAzureContainerClient

cluster_examples = ClusterFactory()


@mock.patch.dict(
    os.environ,
    {
        "AZURE_SUBSCRIPTION_ID": "test_azure_subscription_id",
        "AZURE_TENANT_ID": "test_azure_tenant_id",
        "AZURE_CLIENT_ID": "test_azure_client_id",
        "AZURE_CLIENT_SECRET": "test_azure_client_secret",
    },
    clear=True,
)
def test_container_client_successful_creation() -> None:
    from astrobasecloud.providers.azure import AzureProvider

    azure_provider = AzureProvider()
    # this will still fail because we cant initialize a client
    # without legitimate credentials
    with pytest.raises(HTTPException):
        assert not azure_provider.container_client()


@mock.patch(
    "astrobasecloud.providers.azure.AzureProvider.container_client",
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
    "astrobasecloud.providers.azure.AzureProvider.container_client",
    return_value=MockFailAzureContainerClient(),
)
def test_create_cluster_no_duplicate(
    mock_azure_container_client: mock.MagicMock, client: TestClient
) -> None:
    response = client.post(
        "/azure/cluster", json=cluster_examples.aks_example_complete_spec()
    )
    assert response.status_code == 400
    assert response.json().get("detail").startswith("Create AKS cluster failed with:")


@mock.patch(
    "astrobasecloud.providers.azure.AzureProvider.container_client",
    return_value=MockAzureContainerClient(),
)
def test_get_clusters(
    mock_azure_container_client: mock.MagicMock, client: TestClient
) -> None:
    response = client.get("/azure/cluster?resource_group_name=test-rg")
    assert response.status_code == 200
    assert response.json()[0]["name"] == "my_mock_managed_cluster"


@mock.patch(
    "astrobasecloud.providers.azure.AzureProvider.container_client",
    return_value=MockFailAzureContainerClient(),
)
def test_get_clusters_failure(
    mock_azure_container_client: mock.MagicMock, client: TestClient
) -> None:
    response = client.get("/azure/cluster?resource_group_name=test-rg")
    assert response.status_code == 400
    assert response.json()["detail"].startswith("Get AKS clusters failed for resource ")


@mock.patch(
    "astrobasecloud.providers.azure.AzureProvider.container_client",
    return_value=MockAzureContainerClient(),
)
def test_describe_cluster(
    mock_azure_container_client: mock.MagicMock, client: TestClient
) -> None:
    response = client.get("/azure/cluster/my-cluster?resource_group_name=test-rg")
    assert response.status_code == 200
    assert response.json()["name"] == "my-cluster"


@mock.patch(
    "astrobasecloud.providers.azure.AzureProvider.container_client",
    return_value=MockFailAzureContainerClient(),
)
def test_describe_cluster_failure(
    mock_azure_container_client: mock.MagicMock, client: TestClient
) -> None:
    response = client.get("/azure/cluster/my-cluster?resource_group_name=test-rg")
    assert response.status_code == 400
    assert response.json()["detail"].startswith("Get AKS cluster failed for cluster")


@mock.patch(
    "astrobasecloud.providers.azure.AzureProvider.container_client",
    return_value=MockAzureContainerClient(),
)
def test_delete_cluster(
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


@mock.patch(
    "astrobasecloud.providers.azure.AzureProvider.container_client",
    return_value=MockFailAzureContainerClient(),
)
def test_delete_cluster_failure(
    mock_azure_container_client: mock.MagicMock, client: TestClient
) -> None:
    response = client.delete(
        "/azure/cluster", json=cluster_examples.aks_example_complete_spec()
    )
    assert response.status_code == 400
    assert response.json()["detail"].startswith("Delete AKS cluster failed for cluster")
