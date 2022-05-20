import time
from typing import List

import boto3
from fastapi import HTTPException

from astrobasecloud.exc.main import AstrobaseException
from astrobasecloud.providers._provider import Provider
from astrobasecloud.server.logger import logger
from astrobasecloud.types.aws import (
    EKSCluster,
    EKSClusterAPIFilter,
    EKSClusterDescribeClusterResponse,
    EKSClusterDescribeNodegroupResponse,
    EKSClusterListClustersResponse,
    EKSClusterListNodegroupsResponse,
)


class AWSProvider(Provider):
    RETRY_COUNT = 23
    RETRY_WAIT_SECONDS = 60

    def __init__(self) -> None:
        super().__init__()

    def eks_client(self, region: str) -> boto3.client:
        return boto3.client("eks", region_name=region)

    def create(self, eks_cluster: EKSCluster) -> None:
        cluster_data = EKSClusterAPIFilter(**eks_cluster.dict())
        eks_client = self.eks_client(region=eks_cluster.region)
        cluster = eks_client.create_cluster(**cluster_data.dict())

        if cluster:
            count = 0
            cluster_status = self.cluster_status(
                cluster_data.name, region=eks_cluster.region
            )
            while not self.cluster_is_active(cluster_status=cluster_status):
                if count > self.RETRY_COUNT:
                    msg = (
                        "Something doesn't seem right "
                        f"with cluster {cluster_data.name}. "
                        "Please check the AWS Console for more information."
                    )
                    logger.error(msg=msg)
                    raise AstrobaseException(msg)
                logger.info(
                    f"Waiting {self.RETRY_WAIT_SECONDS} seconds "
                    "before trying to create node group again."
                )
                time.sleep(self.RETRY_WAIT_SECONDS)
                cluster_status = self.cluster_status(
                    cluster_name=cluster_data.name, region=eks_cluster.region
                )
                count += 1

        for nodegroup in eks_cluster.nodegroups:
            eks_client.create_nodegroup(**nodegroup.dict())
        return

    def cluster_status(self, cluster_name: str, region: str) -> str:
        return (
            self.describe(cluster_name=cluster_name, region=region)
            .dict()
            .get("cluster", {})
            .get("status")
        )

    def cluster_is_active(self, cluster_status: str) -> bool:
        return cluster_status == "ACTIVE"

    def get(self, region: str) -> EKSClusterListClustersResponse:
        try:
            return EKSClusterListClustersResponse(
                **self.eks_client(region=region).list_clusters()
            )
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=400, detail=str(e))

    def describe(
        self, cluster_name: str, region: str
    ) -> EKSClusterDescribeClusterResponse:
        try:
            return EKSClusterDescribeClusterResponse(
                **self.eks_client(region=region).describe_cluster(name=cluster_name)
            )
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=400, detail=str(e))

    def list_cluster_nodegroups(
        self, cluster_name: str, region: str
    ) -> EKSClusterListNodegroupsResponse:
        try:
            return EKSClusterListNodegroupsResponse(
                **self.eks_client(region=region).list_nodegroups(
                    clusterName=cluster_name
                )
            )
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=400, detail=str(e))

    def describe_cluster_nodegroup(
        self, cluster_name: str, nodegroup_name: str, region: str
    ) -> EKSClusterDescribeNodegroupResponse:
        try:
            return EKSClusterDescribeNodegroupResponse(
                **self.eks_client(region=region).describe_nodegroup(
                    clusterName=cluster_name, nodegroupName=nodegroup_name
                )
            )
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=400, detail=str(e))

    def delete(
        self, cluster_name: str, nodegroup_names: List[str], region: str
    ) -> None:
        eks_client = self.eks_client(region=region)
        for nodegroup_name in nodegroup_names:
            eks_client.delete_nodegroup(
                clusterName=cluster_name, nodegroupName=nodegroup_name
            )
        count = 0
        while True:
            if count > self.RETRY_COUNT:
                msg = (
                    "Something doesn't seem right "
                    f"with cluster {cluster_name}. "
                    "Please check the AWS Console for more information."
                )
                logger.error(msg=msg)
                raise AstrobaseException(msg)
            try:
                eks_client.delete_cluster(name=cluster_name)
                return
            except Exception as e:
                response_attr = "response"
                if hasattr(e, response_attr):
                    logger.error(getattr(e, response_attr))
                else:
                    logger.error(
                        f"Logging exception that does not have response attr: {e}"
                    )
            count += 1
            logger.info(
                f"Waiting {self.RETRY_WAIT_SECONDS} seconds "
                "before trying to delete cluster again."
            )
            time.sleep(self.RETRY_WAIT_SECONDS)


aws_provider = AWSProvider()
