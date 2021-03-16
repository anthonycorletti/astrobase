import time
from typing import List

import boto3

from astrobase.schemas.eks import EKSCreate, EKSCreateAPIFilter
from config.logger import logger


class EKSApi:
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

    def create(self, cluster_create: EKSCreate) -> dict:
        cluster_data = EKSCreateAPIFilter(**cluster_create.dict())
        try:
            cluster = self.client.create_cluster(**cluster_data.dict())
        except Exception as e:
            logger.error(e)
            logger.info(f"Looking for cluster: {cluster_data.name}")
            cluster = self.describe(cluster_name=cluster_data.name)

        if cluster:
            count = 0
            cluster_status = (
                self.describe(cluster_name=cluster_data.name)
                .get("cluster", {})
                .get("status")
            )
            while cluster_status != "ACTIVE":
                if count > 17:
                    raise Exception(
                        "Something doesn't seem right "
                        f"with cluster {cluster_data.name}"
                    )
                logger.info("waiting before trying to create node group again")
                time.sleep(60)
                cluster_status = (
                    self.describe(cluster_name=cluster_data.name)
                    .get("cluster", {})
                    .get("status")
                )
                count += 1

        for nodegroup in cluster_create.nodegroups:
            try:
                self.client.create_nodegroup(**nodegroup.dict())
            except Exception as e:
                logger.error(e)
        return

    def get(self) -> List[str]:
        return self.client.list_clusters().get("clusters", [])

    def describe(self, cluster_name: str) -> dict:
        try:
            return self.client.describe_cluster(name=cluster_name)
        except Exception as e:
            logger.error(e)

    def delete(self, cluster_name: str, nodegroup_names: List[str]) -> dict:
        for nodegroup_name in nodegroup_names:
            try:
                self.client.delete_nodegroup(
                    clusterName=cluster_name, nodegroupName=nodegroup_name
                )
            except Exception as e:
                logger.error(e.response)
        count = 0
        while True:
            if count > 17:
                raise Exception("Timed out waiting for node groups to delete.")
            try:
                self.client.delete_cluster(name=cluster_name)
                return {
                    "cluster_name": cluster_name,
                    "nodegroup_names": nodegroup_names,
                }
            except Exception as e:
                logger.error(e.response)
            count += 1
            logger.info("waiting before trying to delete cluster again")
            time.sleep(60)
