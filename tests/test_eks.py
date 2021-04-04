import os

from botocore.stub import Stubber

from astrobase.apis.eks import EKSApi
from astrobase.schemas.eks import EKSCreate, EKSCreateAPIFilter
from tests.factories import ClusterFactory

cluster_examples = ClusterFactory()


def test_create_cluster(eks_mock):
    eks_client = eks_mock()
    stubber = Stubber(eks_client)
    eks_stub_dict = EKSCreateAPIFilter(**cluster_examples.eks_example()).dict()
    stubber.add_response("create_cluster", {"cluster": eks_stub_dict})
    stubber.add_response("describe_cluster", {"cluster": {"status": "ACTIVE"}})
    stubber.add_response("create_nodegroup", {"nodegroup": {}})
    stubber.activate()
    eks_api = EKSApi(region=os.environ["AWS_REGION"])
    response = eks_api.create(EKSCreate(**cluster_examples.eks_example()))
    stubber.deactivate()
    assert response is None


def test_get_clusters(eks_mock):
    eks_client = eks_mock()
    stubber = Stubber(eks_client)
    stubber.add_response("list_clusters", {"clusters": ["cluster-0", "cluster-1"]})
    stubber.activate()
    eks_api = EKSApi(region=os.environ["AWS_REGION"])
    response = eks_api.get()
    stubber.deactivate()
    assert response == ["cluster-0", "cluster-1"]


def test_get_cluster(eks_mock):
    eks_client = eks_mock()
    stubber = Stubber(eks_client)
    stubber.add_response("describe_cluster", {"cluster": {"name": "cluster-0"}})
    stubber.activate()
    eks_api = EKSApi(region=os.environ["AWS_REGION"])
    response = eks_api.describe("cluster-0").get("cluster")
    stubber.deactivate()
    assert response == {"name": "cluster-0"}


def test_describe_cluster(client):
    assert False


def test_delete_clister(client):
    assert False
