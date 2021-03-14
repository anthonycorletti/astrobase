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
            logger.error(e.response)
            cluster = e.response
        nodegroups = []
        for nodegroup in cluster_create.nodegroups:
            try:
                nodegroup = self.client.create_nodegroup(**nodegroup.dict())
                nodegroups.append(nodegroup)
            except Exception as e:
                nodegroups.append(e.response)
        return {"cluster_response": cluster, "nodegroups_response": nodegroups}

    def get(self) -> List[str]:
        return self.client.list_clusters().get("clusters", [])

    def describe(self, cluster_name: str) -> dict:
        try:
            return self.client.describe_cluster(name=cluster_name)
        except Exception as e:
            return e.response

    def delete(self, cluster_name: str, nodegroup_names: List[str]) -> dict:
        for nodegroup_name in nodegroup_names:
            try:
                self.client.delete_nodegroup(
                    clusterName=cluster_name, nodegroupName=nodegroup_name
                )
            except Exception as e:
                logger.error(e.response)
        try:
            self.client.delete_cluster(name=cluster_name)
        except Exception as e:
            logger.error(e.response)
        return {
            "cluster_name": cluster_name,
            "nodegroup_names": nodegroup_names,
        }
