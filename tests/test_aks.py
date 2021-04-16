from unittest import mock

from tests.factories import ClusterFactory

cluster_examples = ClusterFactory()


class MockBeginOrCreateResponse:
    def __init__(self, result, status):
        self.result = result
        self.status = status


class MockManagedCluster:
    def __init__(self, name: str = "my_mock_managed_cluster"):
        self.name = name

    def as_dict(self):
        return {"name": self.name}


class MockBeginDeleteResponse:
    def __init__(self, result, status):
        self.result = result
        self.status = status


def test_create_cluster(client):
    with mock.patch(
        "astrobase.apis.aks.AKSApi.make_begin_create_or_update_request"
    ) as mock_make_begin_create_or_update_request:

        mock_make_begin_create_or_update_request.return_value = (
            MockBeginOrCreateResponse(
                result="it worked",
                status="success",
            )
        )

        response = client.post("/aks", json=cluster_examples.aks_example())
        assert response.status_code == 200
        assert response.json().get("result") == "it worked"


def test_get_clusters(client):
    with mock.patch(
        "astrobase.apis.aks.AKSApi.make_get_request"
    ) as mock_make_get_request:

        mock_make_get_request.return_value = [MockManagedCluster()]

        response = client.get("/aks?resource_group_name=my_resource_group")
        assert response.status_code == 200
        assert response.json() == [{"name": "my_mock_managed_cluster"}]


def test_describe_cluster(client):
    with mock.patch("astrobase.apis.aks.AKSApi.describe") as mock_describe:
        cluster_name = "another-cluster"
        mock_describe.return_value = MockManagedCluster(name=cluster_name)

        response = client.get(
            f"/aks/{cluster_name}?resource_group_name=my_resource_group"
        )
        assert response.status_code == 200
        assert response.json() == {"name": "another-cluster"}


def test_delete_clister(client):
    with mock.patch(
        "astrobase.apis.aks.AKSApi.make_begin_delete_request"
    ) as mock_make_begin_delete_request:
        cluster_name = "another-cluster"
        mock_make_begin_delete_request.return_value = MockBeginDeleteResponse(
            result=f"deleting {cluster_name} worked", status="success"
        )

        response = client.delete(
            f"/aks/{cluster_name}?resource_group_name=my_resource_group"
        )
        assert response.status_code == 200
        assert response.json().get("result") == f"deleting {cluster_name} worked"
