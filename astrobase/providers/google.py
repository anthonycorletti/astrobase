from typing import List

from googleapiclient.discovery import build

from astrobase.schemas.cluster import (
    GoogleClusterCreate,
    GoogleClusterCreateAPIFilter,
    GoogleClusterUpdate,
    GoogleClusterUpdateAPIFilter,
)


class GoogleProvider:
    def __init__(self):
        self.client = build("container", "v1beta1")
        self.cluster_client = self.client.projects().zones().clusters()

    def create_cluster(self, cluster_create: GoogleClusterCreate) -> dict:
        filtered_cluster_create = GoogleClusterCreateAPIFilter(**cluster_create.dict())
        body = {"cluster": filtered_cluster_create.dict()}
        req = self.cluster_client.create(
            body={"cluster": body},
            projectId=cluster_create.project_id,
            zone=cluster_create.zone,
        )
        res = req.execute()
        return dict(res)

    def get_clusters(self, project_id: str, zone: str) -> List[dict]:
        req = self.cluster_client.list(zone=zone, projectId=project_id)
        res = req.execute()
        return dict(res)

    def describe_cluster(self, zone: str, project_id: str, cluster_name: str) -> dict:
        req = self.cluster_client.get(
            zone=zone, projectId=project_id, clusterId=cluster_name
        )
        res = req.execute()
        return dict(res)

    def update_cluster(
        self,
        zone: str,
        project_id: str,
        cluster_name: str,
        cluster_update: GoogleClusterUpdate,
    ) -> dict:
        filtered_cluster_update = GoogleClusterUpdateAPIFilter(**cluster_update.dict())
        body = {"name": cluster_name, "update": filtered_cluster_update.dict()}
        req = self.cluster_client.update(
            zone=zone,
            projectId=project_id,
            clusterId=cluster_name,
            cluster=body,
        )
        res = req.execute()
        return dict(res)

    def delete_cluster(
        self,
        zone: str,
        project_id: str,
        cluster_name: str,
    ) -> dict:
        req = self.cluster_client.delete(
            zone=zone, projectId=project_id, clusterId=cluster_name
        )
        res = req.execute()
        return dict(res)
