from fastapi import APIRouter, BackgroundTasks, Body

from astrobasecloud.providers.aws import aws_provider
from astrobasecloud.types.aws import (
    EKSCluster,
    EKSClusterDescribeClusterResponse,
    EKSClusterDescribeNodegroupResponse,
    EKSClusterListClustersResponse,
    EKSClusterListNodegroupsResponse,
    EKSClusterOperationResponse,
)
from astrobasecloud.types.provider import ProviderName

router = APIRouter(tags=[ProviderName.aws], prefix="/aws")


@router.post("/cluster", response_model=EKSClusterOperationResponse)
def create_eks_cluster(
    background_tasks: BackgroundTasks,
    eks_cluster: EKSCluster = Body(...),
) -> EKSClusterOperationResponse:
    background_tasks.add_task(aws_provider.create, eks_cluster)
    return EKSClusterOperationResponse(
        message=f"EKS create request submitted for {eks_cluster.name}"
    )


@router.get("/cluster", response_model=EKSClusterListClustersResponse)
def get_eks_clusters(region: str) -> EKSClusterListClustersResponse:
    return aws_provider.get(region=region)


@router.get("/cluster/{cluster_name}", response_model=EKSClusterDescribeClusterResponse)
def describe_eks_cluster(
    cluster_name: str, region: str
) -> EKSClusterDescribeClusterResponse:
    return aws_provider.describe(cluster_name=cluster_name, region=region)


@router.get(
    "/cluster/{cluster_name}/nodegroup",
    response_model=EKSClusterListNodegroupsResponse,
)
def list_eks_cluster_nodegroups(
    cluster_name: str, region: str
) -> EKSClusterListNodegroupsResponse:
    return aws_provider.list_cluster_nodegroups(
        cluster_name=cluster_name, region=region
    )


@router.get(
    "/cluster/{cluster_name}/nodegroup/{nodegroup_name}",
    response_model=EKSClusterDescribeNodegroupResponse,
)
def describe_eks_cluster_nodegroup(
    cluster_name: str, nodegroup_name: str, region: str
) -> EKSClusterDescribeNodegroupResponse:
    return aws_provider.describe_cluster_nodegroup(
        cluster_name=cluster_name, nodegroup_name=nodegroup_name, region=region
    )


@router.delete("/cluster", response_model=EKSClusterOperationResponse)
def delete_eks_cluster(
    background_tasks: BackgroundTasks, eks_cluster: EKSCluster = Body(...)
) -> EKSClusterOperationResponse:
    nodegroup_names = [ng.nodegroupName for ng in eks_cluster.nodegroups]
    background_tasks.add_task(
        func=aws_provider.delete,
        cluster_name=eks_cluster.name,
        nodegroup_names=nodegroup_names,
        region=eks_cluster.region,
    )
    return EKSClusterOperationResponse(
        message=f"EKS delete request submitted for {eks_cluster.name} cluster"
        f" and nodegroups: {', '.join(nodegroup_names)}"
    )
