from typing import Dict, List

from fastapi import APIRouter, BackgroundTasks, Body

from astrobase.providers.aws import AWSProvider
from astrobase.types.aws import EKSCluster
from astrobase.types.provider import ProviderName

router = APIRouter(tags=[ProviderName.aws], prefix="/aws")


@router.post("/cluster")
def create_eks_cluster(
    background_tasks: BackgroundTasks,
    eks_cluster: EKSCluster = Body(...),
) -> Dict:
    aws_provider = AWSProvider(region=eks_cluster.region)
    background_tasks.add_task(aws_provider.create, eks_cluster)
    return {"message": f"EKS create request submitted for {eks_cluster.name}"}


@router.get("/cluster")
def get_eks_clusters(region: str) -> List[str]:
    aws_provider = AWSProvider(region=region)
    return aws_provider.get()


@router.get("/cluster/{cluster_name}")
def describe_eks_cluster(cluster_name: str, region: str) -> Dict:
    aws_provider = AWSProvider(region=region)
    return aws_provider.describe(cluster_name=cluster_name)


@router.get("/cluster/{cluster_name}/nodegroups")
def list_eks_cluster_nodegroups(cluster_name: str, region: str) -> List[Dict]:
    aws_provider = AWSProvider(region=region)
    return aws_provider.list_cluster_nodegroups(cluster_name=cluster_name)


@router.get("/cluster/{cluster_name}/nodegroups/{nodegroup_name}")
def describe_eks_cluster_nodegroup(
    cluster_name: str, nodegroup_name: str, region: str
) -> List[Dict]:
    aws_provider = AWSProvider(region=region)
    return aws_provider.describe_cluster_nodegroup(
        cluster_name=cluster_name, nodegroup_name=nodegroup_name
    )


@router.delete("/cluster")
def delete_eks_cluster(
    background_tasks: BackgroundTasks, eks_cluster: EKSCluster = Body(...)
) -> Dict:
    aws_provider = AWSProvider(region=eks_cluster.region)
    nodegroup_names = [ng.nodegroupName for ng in eks_cluster.nodegroups]
    background_tasks.add_task(
        aws_provider.delete,
        cluster_name=eks_cluster.name,
        nodegroup_names=nodegroup_names,
    )
    return {
        "message": f"EKS delete request submitted for {eks_cluster.name} cluster"
        f" and nodegroups: {', '.join(nodegroup_names)}"
    }
