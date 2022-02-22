from typing import List

from fastapi import APIRouter, BackgroundTasks, Body

from astrobase.providers.aws import AWSProvider
from astrobase.types.aws import EKSCreate
from astrobase.types.provider import ProviderName

router = APIRouter(tags=[ProviderName.aws], prefix="/aws")


@router.post("/eks")
def create_eks_cluster(
    background_tasks: BackgroundTasks,
    cluster_create: EKSCreate = Body(...),
) -> dict:
    aws_provider = AWSProvider(region=cluster_create.region)
    background_tasks.add_task(aws_provider.create, cluster_create)
    return {"message": f"EKS create request submitted for {cluster_create.name}"}


@router.get("/eks")
def get_eks_clusters(region: str) -> List[str]:
    aws_provider = AWSProvider(region=region)
    return aws_provider.get()


@router.get("/eks/{cluster_name}")
def describe_eks_cluster(cluster_name: str, region: str) -> dict:
    aws_provider = AWSProvider(region=region)
    return aws_provider.describe(cluster_name=cluster_name)


@router.get("/eks/{cluster_name}/nodegroups")
def list_eks_cluster_nodegroups(cluster_name: str, region: str) -> List[dict]:
    aws_provider = AWSProvider(region=region)
    return aws_provider.list_cluster_nodegroups(cluster_name=cluster_name)


@router.get("/eks/{cluster_name}/nodegroups/{nodegroup_name}")
def describe_eks_cluster_nodegroup(
    cluster_name: str, nodegroup_name: str, region: str
) -> List[dict]:
    aws_provider = AWSProvider(region=region)
    return aws_provider.describe_cluster_nodegroup(
        cluster_name=cluster_name, nodegroup_name=nodegroup_name
    )


@router.delete("/eks/{cluster_name}")
def delete_eks_cluster(
    cluster_name: str,
    region: str,
    background_tasks: BackgroundTasks,
    nodegroup_names: List[str] = Body(..., example=[]),
) -> dict:
    aws_provider = AWSProvider(region=region)
    background_tasks.add_task(
        aws_provider.delete, cluster_name=cluster_name, nodegroup_names=nodegroup_names
    )
    return {
        "message": f"EKS delete request submitted for {cluster_name} cluster"
        f" and nodegroups: {', '.join(nodegroup_names)}"
    }
