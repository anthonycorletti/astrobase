from typing import List

import boto3

from astrobase.schemas.eks import EKSCreate
from config.logger import logger


class EKSApi:
    def __init__(self):
        try:
            self.client = boto3.client("eks")
        except Exception as e:
            logger.error("Exception: ", e)
            logger.error(
                "Missing credentials for EKSApi. ",
                "Make sure you've set your ",
                "AWS_PROFILE environment variable and have ",
                "specificed those credentials in ~/.aws/credentials.",
            )

    def create(self, cluster_create: EKSCreate) -> dict:
        return self.client.create_cluster(**cluster_create.dict())

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
