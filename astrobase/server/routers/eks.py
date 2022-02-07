from typing import Dict, List

from fastapi import APIRouter, BackgroundTasks, Body

from astrobase.providers.eks import EKSApi
from astrobase.schemas.eks import EKSCreate

router = APIRouter()
tags = ["cluster", "eks"]


@router.post("/eks", tags=tags)
def create_eks_cluster(
    background_tasks: BackgroundTasks,
    cluster_create: EKSCreate = Body(...),
) -> Dict:
    eks_api = EKSApi(region=cluster_create.region)
    background_tasks.add_task(eks_api.create, cluster_create)
    return {"message": f"EKS create request submitted for {cluster_create.name}"}


@router.get("/eks", tags=tags)
def get_eks_clusters(region: str) -> List[str]:
    eks_api = EKSApi(region=region)
    return eks_api.get()


@router.get("/eks/{cluster_name}", tags=tags)
def describe_eks_cluster(cluster_name: str, region: str) -> Dict:
    eks_api = EKSApi(region=region)
    return eks_api.describe(cluster_name=cluster_name)


@router.get("/eks/{cluster_name}/nodegroups", tags=tags)
def list_eks_cluster_nodegroups(cluster_name: str, region: str) -> List[Dict]:
    eks_api = EKSApi(region=region)
    return eks_api.list_cluster_nodegroups(cluster_name=cluster_name)


@router.get("/eks/{cluster_name}/nodegroups/{nodegroup_name}", tags=tags)
def describe_eks_cluster_nodegroup(
    cluster_name: str, nodegroup_name: str, region: str
) -> List[Dict]:
    eks_api = EKSApi(region=region)
    return eks_api.describe_cluster_nodegroup(
        cluster_name=cluster_name, nodegroup_name=nodegroup_name
    )


@router.delete("/eks/{cluster_name}", tags=tags)
def delete_eks_cluster(
    cluster_name: str,
    region: str,
    background_tasks: BackgroundTasks,
    nodegroup_names: List[str] = Body(..., example=[]),
) -> Dict:
    eks_api = EKSApi(region=region)
    background_tasks.add_task(
        eks_api.delete, cluster_name=cluster_name, nodegroup_names=nodegroup_names
    )
    return {
        "message": f"EKS delete request submitted for {cluster_name} cluster"
        f" and nodegroups: {', '.join(nodegroup_names)}"
    }
