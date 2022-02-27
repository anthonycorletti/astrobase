import os
from typing import Any

from botocore.stub import Stubber
from fastapi.testclient import TestClient

from astrobase.types.aws import (
    EKSCluster,
    EKSClusterAPIFilter,
    EKSDescribeClusterAPIFilter,
)
from tests.factories import ClusterFactory

cluster_examples = ClusterFactory()


def test_create_cluster(client: TestClient, mock_eks_client: Any) -> None:
    eks_client = mock_eks_client()
    stubber = Stubber(eks_client)
    mock_eks_create_body = EKSClusterAPIFilter(
        **cluster_examples.eks_example_complete_spec()
    ).dict()
    stubber.add_response("create_cluster", {"cluster": mock_eks_create_body})
    mock_eks_create_body["status"] = "ACTIVE"
    stubber.add_response("describe_cluster", {"cluster": mock_eks_create_body})
    stubber.add_response(
        "create_nodegroup",
        {"nodegroup": cluster_examples.eks_example_complete_spec()["nodegroups"][0]},
    )
    stubber.activate()
    response = client.post(
        "/aws/cluster", json=cluster_examples.eks_example_complete_spec()
    )
    stubber.deactivate()
    assert response.status_code == 200


def test_create_cluster_random_cluster_name() -> None:
    example = cluster_examples.eks_example_complete_spec()
    del example["name"]
    eks_create = EKSCluster(**example)
    assert eks_create.name is not None
    assert eks_create.name != cluster_examples.eks_example()["name"]


def test_get_clusters(client: TestClient, mock_eks_client: Any) -> None:
    eks_client = mock_eks_client()
    stubber = Stubber(eks_client)
    response_data = {"clusters": ["cluster-0", "cluster-1"]}
    stubber.add_response("list_clusters", response_data)
    stubber.activate()
    response = client.get(f"/aws/cluster?region={os.environ['AWS_REGION']}")
    stubber.deactivate()
    assert response.status_code == 200
    assert response.json() == response_data


def test_get_cluster(client: TestClient, mock_eks_client: Any) -> None:
    eks_client = mock_eks_client()
    stubber = Stubber(eks_client)
    data = cluster_examples.eks_example_complete_spec()
    data["status"] = "ACTIVE"
    response_data = EKSDescribeClusterAPIFilter(**data)
    stubber.add_response("describe_cluster", {"cluster": response_data.dict()})
    stubber.activate()
    response = client.get(
        f"/aws/cluster/{response_data.name}?region={os.environ['AWS_REGION']}"
    )
    stubber.deactivate()
    assert response.status_code == 200
    assert response.json()["cluster"] == response_data


def test_get_cluster_nodegroups(client: TestClient, mock_eks_client: Any) -> None:
    eks_client = mock_eks_client()
    stubber = Stubber(eks_client)
    stubber.add_response("list_nodegroups", {"nodegroups": ["nodegroup-0"]})
    stubber.activate()
    response = client.get(
        f"/aws/cluster/cluster-0/nodegroup?region={os.environ['AWS_REGION']}"
    )
    stubber.deactivate()
    assert response.status_code == 200
    assert response.json() == {"nodegroups": ["nodegroup-0"]}


def test_describe_cluster_nodegroup(client: TestClient, mock_eks_client: Any) -> None:
    eks_client = mock_eks_client()
    data = cluster_examples.eks_example_complete_spec()
    stubber = Stubber(eks_client)
    stubber.add_response("describe_nodegroup", {"nodegroup": data["nodegroups"][0]})
    stubber.activate()
    response = client.get(
        f"/aws/cluster/cluster-0/nodegroup/"
        f"nodegroup-0?region={os.environ['AWS_REGION']}"
    )
    stubber.deactivate()
    assert response.status_code == 200
    assert (
        response.json()["nodegroup"]["nodegroupName"]
        == data["nodegroups"][0]["nodegroupName"]
    )


def test_delete_cluster(client: TestClient, mock_eks_client: Any) -> None:
    eks_client = mock_eks_client()
    stubber = Stubber(eks_client)
    stubber.add_response(
        "delete_nodegroup", {"nodegroup": {"nodegroupName": "nodegroup-0"}}
    )
    stubber.add_response("delete_cluster", {"cluster": {"name": "cluster-0"}})
    stubber.activate()
    response = client.delete(
        "/aws/cluster", json=cluster_examples.eks_example_complete_spec()
    )
    stubber.deactivate()
    assert response.status_code == 200
    assert (
        response.json()["message"] == "EKS delete request submitted for "
        "my-eks-cluster cluster and nodegroups: main"
    )
