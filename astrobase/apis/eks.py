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
        return self.client.create_cluster(**cluster_data.dict())

    def get(self) -> List[str]:
        return self.client.list_clusters().get("clusters", [])

    def describe(self, cluster_name: str) -> dict:
        try:
            return self.client.describe_cluster(name=cluster_name)
        except Exception as e:
            return e.response

    def delete(self, cluster_name: str) -> dict:
        try:
            return self.client.delete_cluster(name=cluster_name)
        except Exception as e:
            return e.response
