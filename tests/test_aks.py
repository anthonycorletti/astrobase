from unittest import mock

from tests.factories import ClusterFactory

cluster_examples = ClusterFactory()


def test_create_cluster(client):
    with mock.patch("astrobase.apis.aks.AKSApi.create") as mock_begin_or_create:  # noqa

        class MockBeginOrCreateResponse:
            def __init__(self, result, status):
                self.result = result
                self.status = status

        mock_begin_or_create.return_value = MockBeginOrCreateResponse(
            result="it worked",
            status="success",
        )

        response = client.post("/aks", json=cluster_examples.aks_example())
        assert response.status_code == 200
        assert response.json().get("result") == "it worked"


def test_get_clusters(client):
    pass


def test_describe_cluster(client):
    pass


def test_delete_clister(client):
    pass
