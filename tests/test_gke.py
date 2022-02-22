from unittest import mock

from fastapi.testclient import TestClient

from tests.factories import ClusterFactory

cluster_examples = ClusterFactory()


def test_create_cluster(client: TestClient) -> None:
    with mock.patch(
        "astrobase.providers.gcp.GCPProvider.create_cluster_async"
    ) as mock_gke_api_request:
        mock_gke_api_request.return_value = {"name": "astrobase-gke-api"}
        response = client.post("/gcp/cluster", json=cluster_examples.gke_example())
        assert response.status_code == 200
        assert response.json().get("name") == "astrobase-gke-api"


def test_get_clusters(client: TestClient) -> None:
    with mock.patch("astrobase.providers.gcp.GCPProvider.get") as mock_gke_api_request:
        mock_gke_api_request.return_value = {"name": "astrobase-gke-api"}
        response = client.get(
            "/gcp/cluster?project_id=test&location=us-central1",
            json=cluster_examples.gke_example(),
        )
        assert response.status_code == 200
        assert response.json().get("name") == "astrobase-gke-api"


def test_delete_clister(client: TestClient) -> None:
    with mock.patch("astrobase.providers.gcp.GCPProvider.delete_cluster_async"):
        response = client.delete(
            "/gcp/cluster",
            json=cluster_examples.gke_example(),
        )
        assert response.status_code == 200
