import os
from typing import Any
from unittest import mock

import pytest
from botocore.stub import Stubber
from fastapi.testclient import TestClient

from astrobasecloud.exc.main import AstrobaseException
from astrobasecloud.types.aws import (
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


@mock.patch(
    "astrobasecloud.providers.aws.AWSProvider.RETRY_COUNT",
    new_callable=mock.PropertyMock,
    return_value=-1,
)
def test_create_cluster_failed(
    mock_aws_provider: mock.MagicMock,
    client: TestClient,
    mock_eks_client: Any,
) -> None:
    eks_client = mock_eks_client()
    stubber = Stubber(eks_client)
    mock_eks_create_body = EKSClusterAPIFilter(
        **cluster_examples.eks_example_complete_spec()
    ).dict()
    stubber.add_response("create_cluster", {"cluster": mock_eks_create_body})
    mock_eks_create_body["status"] = "NOTACTIVE"
    stubber.add_response("describe_cluster", {"cluster": mock_eks_create_body})
    stubber.activate()
    with pytest.raises(AstrobaseException):
        client.post("/aws/cluster", json=cluster_examples.eks_example_complete_spec())
    stubber.deactivate()


@mock.patch(
    "astrobasecloud.providers.aws.AWSProvider.RETRY_COUNT",
    new_callable=mock.PropertyMock,
    return_value=0,
)
@mock.patch(
    "astrobasecloud.providers.aws.AWSProvider.RETRY_WAIT_SECONDS",
    new_callable=mock.PropertyMock,
    return_value=1,
)
def test_create_cluster_failed_eventually(
    mock_aws_provider_retry_count: mock.MagicMock,
    mock_aws_provider_retry_wait_seconds: mock.MagicMock,
    client: TestClient,
    mock_eks_client: Any,
) -> None:
    eks_client = mock_eks_client()
    stubber = Stubber(eks_client)
    mock_eks_create_body = EKSClusterAPIFilter(
        **cluster_examples.eks_example_complete_spec()
    ).dict()
    stubber.add_response("create_cluster", {"cluster": mock_eks_create_body})
    mock_eks_create_body["status"] = "NOTACTIVE"
    stubber.add_response("describe_cluster", {"cluster": mock_eks_create_body})
    stubber.add_response("describe_cluster", {"cluster": mock_eks_create_body})
    stubber.activate()
    with pytest.raises(AstrobaseException):
        client.post("/aws/cluster", json=cluster_examples.eks_example_complete_spec())
    stubber.deactivate()


def test_create_cluster_random_cluster_name() -> None:
    example = cluster_examples.eks_example_complete_spec()
    eks_create = EKSCluster(**example)
    assert eks_create.name == "my-eks-cluster"


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


def test_get_clusters_raises(client: TestClient, mock_eks_client: Any) -> None:
    eks_client = mock_eks_client()
    stubber = Stubber(eks_client)
    stubber.add_client_error("list_clusters", service_message="Whoops!")
    stubber.activate()
    response = client.get(f"/aws/cluster?region={os.environ['AWS_REGION']}")
    stubber.deactivate()
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "An error occurred () when calling the ListClusters operation: Whoops!"
    )


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


def test_get_cluster_raises(client: TestClient, mock_eks_client: Any) -> None:
    eks_client = mock_eks_client()
    stubber = Stubber(eks_client)
    data = cluster_examples.eks_example_complete_spec()
    data["status"] = "ACTIVE"
    response_data = EKSDescribeClusterAPIFilter(**data)
    stubber.add_client_error("describe_cluster", service_message="Whoops!")
    stubber.activate()
    response = client.get(
        f"/aws/cluster/{response_data.name}?region={os.environ['AWS_REGION']}"
    )
    stubber.deactivate()
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "An error occurred () when calling the DescribeCluster operation: Whoops!"
    )


def test_get_cluster_nodegroups(client: TestClient, mock_eks_client: Any) -> None:
    eks_client = mock_eks_client()
    stubber = Stubber(eks_client)
    stubber.add_client_error("list_nodegroups", service_message="Whoops!")
    stubber.activate()
    response = client.get(
        f"/aws/cluster/cluster-0/nodegroup?region={os.environ['AWS_REGION']}"
    )
    stubber.deactivate()
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "An error occurred () when calling the ListNodegroups operation: Whoops!"
    )


def test_describe_cluster_nodegroup(client: TestClient, mock_eks_client: Any) -> None:
    eks_client = mock_eks_client()
    stubber = Stubber(eks_client)
    stubber.add_client_error("describe_nodegroup", service_message="Whoops!")
    stubber.activate()
    response = client.get(
        f"/aws/cluster/cluster-0/nodegroup/"
        f"nodegroup-0?region={os.environ['AWS_REGION']}"
    )
    stubber.deactivate()
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "An error occurred () when calling the DescribeNodegroup operation: Whoops!"
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


@mock.patch(
    "astrobasecloud.providers.aws.AWSProvider.RETRY_COUNT",
    new_callable=mock.PropertyMock,
    return_value=-1,
)
def test_delete_cluster_failed(
    mock_aws_provider: mock.MagicMock, client: TestClient, mock_eks_client: Any
) -> None:
    eks_client = mock_eks_client()
    stubber = Stubber(eks_client)
    stubber.add_response(
        "delete_nodegroup", {"nodegroup": {"nodegroupName": "nodegroup-0"}}
    )
    stubber.add_response("delete_cluster", {"cluster": {"name": "cluster-0"}})
    stubber.activate()
    with pytest.raises(AstrobaseException):
        client.delete("/aws/cluster", json=cluster_examples.eks_example_complete_spec())
    stubber.deactivate()


@mock.patch(
    "astrobasecloud.providers.aws.AWSProvider.RETRY_COUNT",
    new_callable=mock.PropertyMock,
    return_value=0,
)
@mock.patch(
    "astrobasecloud.providers.aws.AWSProvider.RETRY_WAIT_SECONDS",
    new_callable=mock.PropertyMock,
    return_value=1,
)
def test_delete_cluster_failed_eventually(
    mock_aws_provider_retry_count: mock.MagicMock,
    mock_aws_provider_retry_wait_seconds: mock.MagicMock,
    client: TestClient,
    mock_eks_client: Any,
) -> None:
    eks_client = mock_eks_client()
    stubber = Stubber(eks_client)
    stubber.add_response(
        "delete_nodegroup", {"nodegroup": {"nodegroupName": "nodegroup-0"}}
    )
    stubber.add_client_error("delete_cluster", service_message="Whoops!")
    stubber.add_response("delete_cluster", {"cluster": {"name": "cluster-0"}})
    stubber.activate()
    with pytest.raises(AstrobaseException):
        client.delete("/aws/cluster", json=cluster_examples.eks_example_complete_spec())
    stubber.deactivate()


@mock.patch(
    "astrobasecloud.providers.aws.AWSProvider.RETRY_COUNT",
    new_callable=mock.PropertyMock,
    return_value=0,
)
@mock.patch(
    "astrobasecloud.providers.aws.AWSProvider.RETRY_WAIT_SECONDS",
    new_callable=mock.PropertyMock,
    return_value=1,
)
def test_delete_cluster_failed_eventually_with_response(
    mock_aws_provider_retry_count: mock.MagicMock,
    mock_aws_provider_retry_wait_seconds: mock.MagicMock,
    client: TestClient,
    mock_eks_client: Any,
) -> None:
    eks_client = mock_eks_client()
    stubber = Stubber(eks_client)
    stubber.add_response(
        "delete_nodegroup", {"nodegroup": {"nodegroupName": "nodegroup-0"}}
    )
    stubber.add_client_error(
        "delete_cluster",
        expected_params={"response": "Whoops!"},
        service_message={"response": "Whoops!"},
    )
    stubber.add_response("delete_cluster", {"cluster": {"name": "cluster-0"}})
    stubber.activate()
    with pytest.raises(AstrobaseException):
        client.delete("/aws/cluster", json=cluster_examples.eks_example_complete_spec())
    stubber.deactivate()
