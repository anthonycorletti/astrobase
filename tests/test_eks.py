import os

from botocore.stub import Stubber

from astrobase.schemas.eks import EKSCreateAPIFilter
from tests.factories import ClusterFactory

cluster_examples = ClusterFactory()


def test_create_cluster(client, eks_mock):
    eks_client = eks_mock()
    stubber = Stubber(eks_client)
    eks_stub_dict = EKSCreateAPIFilter(**cluster_examples.eks_example()).dict()
    stubber.add_response("create_cluster", {"cluster": eks_stub_dict})
    stubber.add_response("describe_cluster", {"cluster": {"status": "ACTIVE"}})
    stubber.add_response("create_nodegroup", {"nodegroup": {}})
    stubber.activate()
    response = client.post("/eks", json=cluster_examples.eks_example())
    stubber.deactivate()
    assert response.status_code == 200
    assert response.json() == {
        "message": "EKS create request submitted "
        f"for {cluster_examples.eks_example().get('name')}"
    }


def test_get_clusters(client, eks_mock):
    eks_client = eks_mock()
    stubber = Stubber(eks_client)
    stubber.add_response("list_clusters", {"clusters": ["cluster-0", "cluster-1"]})
    stubber.activate()
    response = client.get(f"/eks?region={os.environ['AWS_REGION']}")
    stubber.deactivate()
    assert response.status_code == 200
    assert response.json() == ["cluster-0", "cluster-1"]


def test_get_cluster(client, eks_mock):
    eks_client = eks_mock()
    stubber = Stubber(eks_client)
    stubber.add_response("describe_cluster", {"cluster": {"name": "cluster-0"}})
    stubber.activate()
    response = client.get(f"/eks/cluster-0?region={os.environ['AWS_REGION']}")
    stubber.deactivate()
    assert response.status_code == 200
    assert response.json() == {"cluster": {"name": "cluster-0"}}


def test_describe_cluster_nodegroups(client, eks_mock):
    eks_client = eks_mock()
    stubber = Stubber(eks_client)
    stubber.add_response("list_nodegroups", {"nodegroups": ["nodegroup-0"]})
    stubber.activate()
    response = client.get(
        f"/eks/cluster-0/nodegroups?region={os.environ['AWS_REGION']}"
    )
    stubber.deactivate()
    assert response.status_code == 200
    assert response.json() == {"nodegroups": ["nodegroup-0"]}


def test_describe_cluster_nodegroup(client, eks_mock):
    eks_client = eks_mock()
    stubber = Stubber(eks_client)
    stubber.add_response(
        "describe_nodegroup", {"nodegroup": {"nodegroupName": "nodegroup-0"}}
    )
    stubber.activate()
    response = client.get(
        f"/eks/cluster-0/nodegroups/nodegroup-0?region={os.environ['AWS_REGION']}"
    )
    stubber.deactivate()
    assert response.status_code == 200
    assert response.json() == {"nodegroup": {"nodegroupName": "nodegroup-0"}}


def test_delete_cluster(client, eks_mock):
    eks_client = eks_mock()
    stubber = Stubber(eks_client)
    stubber.add_response(
        "delete_nodegroup", {"nodegroup": {"nodegroupName": "nodegroup-0"}}
    )
    stubber.add_response("delete_cluster", {"cluster": {"name": "cluster-0"}})
    stubber.activate()
    response = client.delete(
        f"/eks/cluster-0?region={os.environ['AWS_REGION']}",
        json=["nodegroup-0", "nodegroup-1"],
    )
    stubber.deactivate()
    assert response.status_code == 200
    assert response.json() == {
        "message": "EKS delete request submitted for cluster-0 cluster"
        " and nodegroups: nodegroup-0, nodegroup-1"
    }
