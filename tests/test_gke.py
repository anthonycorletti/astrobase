from unittest import mock

from tests.factories import ClusterFactory

cluster_examples = ClusterFactory()


def test_create_cluster(client):
    with mock.patch(
        "astrobase.providers.gke.GKEApi.make_create_request"
    ) as mock_gke_api_request:
        mock_gke_api_request.return_value = {"name": "astrobase-gke-api"}
        response = client.post("/gcp", json=cluster_examples.gke_example())
        assert response.status_code == 200
        assert response.json().get("name") == "astrobase-gke-api"


def test_get_clusters(client):
    with mock.patch(
        "astrobase.providers.gke.GKEApi.make_get_request"
    ) as mock_gke_api_request:
        mock_gke_api_request.return_value = {"name": "astrobase-gke-api"}
        response = client.get(
            "/gcp?project_id=test&location=us-central1",
            json=cluster_examples.gke_example(),
        )
        assert response.status_code == 200
        assert response.json().get("name") == "astrobase-gke-api"


def test_describe_cluster(client):
    with mock.patch(
        "astrobase.providers.gke.GKEApi.make_describe_request"
    ) as mock_gke_api_request:
        mock_gke_api_request.return_value = {"name": "astrobase-gke-api"}
        response = client.get(
            "/gcp/astrobase-gke-api?project_id=test&location=us-central1"
        )
        assert response.status_code == 200
        assert response.json().get("name") == "astrobase-gke-api"


def test_delete_clister(client):
    with mock.patch("astrobase.providers.gke.GKEApi.make_delete_request"):
        response = client.delete(
            "/gcp/astrobase-gke-api?project_id=test&location=us-central1"
        )
        assert response.status_code == 200
