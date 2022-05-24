from unittest import mock

from fastapi.testclient import TestClient

from tests.factories import ClusterFactory, GCPSetupSpecFactory
from tests.mocks import (
    MockGKEClusterManagerClient,
    MockGKEClusterManagerFailClient,
    MockGKEServiceUsageClient,
    MockGKEServiceUsageFailClient,
)

cluster_examples = ClusterFactory()
gcp_setup_spec_examples = GCPSetupSpecFactory()


@mock.patch(
    "astrobasecloud.providers.gcp.GCPProvider._cluster_manager_client",
    return_value=MockGKEClusterManagerClient,
)
def test_create_cluster(
    mock_cluster_manager_client: mock.MagicMock,
    client: TestClient,
) -> None:
    response = client.post(
        "/gcp/cluster",
        json=cluster_examples.gke_example_complete_spec(),
    )
    assert response.status_code == 200
    assert response.json() == {
        "operation": "createcluster",
        "self_link": "https://google.com",
        "target_link": "https://google.com",
    }


@mock.patch(
    "astrobasecloud.providers.gcp.GCPProvider._cluster_manager_client",
    return_value=MockGKEClusterManagerClient,
)
def test_get_clusters(
    mock_cluster_manager_client: mock.MagicMock, client: TestClient
) -> None:
    response = client.get("/gcp/cluster?project_id=test&location=us-central1")
    assert response.status_code == 200
    assert response.json()[0].get("name") == "my-test-cluster"


@mock.patch(
    "astrobasecloud.providers.gcp.GCPProvider._cluster_manager_client",
    return_value=MockGKEClusterManagerClient,
)
@mock.patch(
    "astrobasecloud.providers.gcp.MessageToDict",
    return_value=cluster_examples.gke_example_complete_spec(),
)
def test_describe_cluster(
    mock_cluster: mock.MagicMock,
    mock_cluster_manager_client: mock.MagicMock,
    client: TestClient,
) -> None:
    response = client.get(
        "/gcp/cluster/my-test-cluster?project_id=test&location=us-central1",
    )
    assert response.status_code == 200
    assert response.json().get("name") == "my-gke-cluster"


@mock.patch(
    "astrobasecloud.providers.gcp.GCPProvider._cluster_manager_client",
    return_value=MockGKEClusterManagerClient,
)
def test_delete_clister(
    mock_cluster_manager_client: mock.MagicMock, client: TestClient
) -> None:
    response = client.delete(
        "/gcp/cluster", json=cluster_examples.gke_example_complete_spec()
    )
    assert response.status_code == 200


@mock.patch(
    "astrobasecloud.providers.gcp.GCPProvider._service_usage_client",
    return_value=MockGKEServiceUsageClient,
)
def test_setup_container_api(
    mock_service_usage_client: mock.MagicMock, client: TestClient
) -> None:
    response = client.post(
        "/gcp/setup", json=gcp_setup_spec_examples.setup_container_api_spec().dict()
    )
    assert response.status_code == 200


@mock.patch(
    "astrobasecloud.providers.gcp.GCPProvider._cluster_manager_client",
    return_value=MockGKEClusterManagerFailClient,
)
def test_create_cluster_raises(
    mock_cluster_manager_client: mock.MagicMock,
    client: TestClient,
) -> None:
    response = client.post(
        "/gcp/cluster",
        json=cluster_examples.gke_example_complete_spec(),
    )
    assert response.status_code == 500


@mock.patch(
    "astrobasecloud.providers.gcp.GCPProvider._cluster_manager_client",
    return_value=MockGKEClusterManagerFailClient,
)
def test_get_clusters_raises(
    mock_cluster_manager_client: mock.MagicMock, client: TestClient
) -> None:
    response = client.get("/gcp/cluster?project_id=test&location=us-central1")
    assert response.status_code == 500


@mock.patch(
    "astrobasecloud.providers.gcp.GCPProvider._cluster_manager_client",
    return_value=MockGKEClusterManagerFailClient,
)
def test_describe_cluster_raises(
    mock_cluster_manager_client: mock.MagicMock, client: TestClient
) -> None:
    response = client.get(
        "/gcp/cluster/my-test-cluster?project_id=test&location=us-central1",
    )
    assert response.status_code == 500


@mock.patch(
    "astrobasecloud.providers.gcp.GCPProvider._cluster_manager_client",
    return_value=MockGKEClusterManagerFailClient,
)
def test_delete_clister_raises(
    mock_cluster_manager_client: mock.MagicMock, client: TestClient
) -> None:
    response = client.delete(
        "/gcp/cluster", json=cluster_examples.gke_example_complete_spec()
    )
    assert response.status_code == 500


@mock.patch(
    "astrobasecloud.providers.gcp.GCPProvider._service_usage_client",
    return_value=MockGKEServiceUsageFailClient,
)
def test_setup_container_api_raises(
    mock_service_usage_client: mock.MagicMock, client: TestClient
) -> None:
    response = client.post(
        "/gcp/setup", json=gcp_setup_spec_examples.setup_container_api_spec().dict()
    )
    assert response.status_code == 500
