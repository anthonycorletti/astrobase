import time
from typing import List

import boto3
from fastapi import HTTPException

from astrobase.providers._provider import Provider
from astrobase.server.logger import logger
from astrobase.types.aws import EKSCluster, EKSClusterAPIFilter


class AWSProvider(Provider):
    RETRY_COUNT = 23

    def __init__(self, region: str):
        self.region = region
        try:
            self.client = boto3.client("eks", region_name=self.region)
        except Exception as e:
            logger.error("Exception: ", e)
            logger.error(
                "Missing credentials for EKSApi. ",
                "Make sure you've set your ",
                "AWS_PROFILE environment variable and have ",
                "specificed those credentials in ~/.aws/credentials.",
            )

    def create(self, eks_cluster: EKSCluster) -> None:
        cluster_data = EKSClusterAPIFilter(**eks_cluster.dict())
        cluster = self.client.create_cluster(**cluster_data.dict())

        if cluster:
            count = 0
            cluster_status = self.cluster_status(cluster_data.name)
            while cluster_status != "ACTIVE":
                if count > self.RETRY_COUNT:
                    raise HTTPException(
                        status_code=400,
                        detail="Something doesn't seem right "
                        f"with cluster {cluster_data.name}",
                    )
                logger.info("waiting before trying to create node group again")
                time.sleep(60)
                cluster_status = self.cluster_status(cluster_data.name)
                count += 1

        for nodegroup in eks_cluster.nodegroups:
            try:
                self.client.create_nodegroup(**nodegroup.dict())
            except Exception as e:
                logger.error(e)
        return

    def cluster_status(self, cluster_name: str) -> str:
        return self.describe(cluster_name=cluster_name).get("cluster", {}).get("status")

    def get(self) -> List[str]:
        try:
            return self.client.list_clusters().get("clusters", [])
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=400, detail=str(e))

    def describe(self, cluster_name: str) -> dict:
        try:
            return self.client.describe_cluster(name=cluster_name)
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=400, detail=str(e))

    def list_cluster_nodegroups(self, cluster_name: str) -> List[dict]:
        try:
            return self.client.list_nodegroups(clusterName=cluster_name)
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=400, detail=str(e))

    def describe_cluster_nodegroup(
        self, cluster_name: str, nodegroup_name: str
    ) -> List[dict]:
        try:
            return self.client.describe_nodegroup(
                clusterName=cluster_name, nodegroupName=nodegroup_name
            )
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=400, detail=str(e))

    def delete(self, cluster_name: str, nodegroup_names: List[str]) -> dict:
        for nodegroup_name in nodegroup_names:
            try:
                self.client.delete_nodegroup(
                    clusterName=cluster_name, nodegroupName=nodegroup_name
                )
            except Exception as e:
                response_attr = "response"
                if hasattr(e, response_attr):
                    logger.error(getattr(e, response_attr))
                else:
                    logger.error(
                        f"Logging exception that does not have response attr: {e}"
                    )
        count = 0
        while True:
            if count > self.RETRY_COUNT:
                raise HTTPException(
                    status_code=400,
                    detail="Timed out waiting for node groups to delete.",
                )
            try:
                self.client.delete_cluster(name=cluster_name)
                return {
                    "cluster_name": cluster_name,
                    "nodegroup_names": nodegroup_names,
                }
            except Exception as e:
                response_attr = "response"
                if hasattr(e, response_attr):
                    logger.error(getattr(e, response_attr))
                else:
                    logger.error(
                        f"Logging exception that does not have response attr: {e}"
                    )
            count += 1
            logger.info("waiting before trying to delete cluster again")
            time.sleep(60)
