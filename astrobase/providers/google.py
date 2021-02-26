from typing import List

from googleapiclient.discovery import build

from astrobase.schemas.cluster import (
    GKECreate,
    GKECreateAPIFilter,
    GKEUpdate,
    GKEUpdateAPIFilter,
)


class GoogleProvider:
    def __init__(self):
        self.client = build("container", "v1beta1")
        self.cluster_client = self.client.projects().zones().clusters()

    def create_gke_cluster(self, cluster_create: GKECreate) -> dict:
        filtered_cluster_create = GKECreateAPIFilter(**cluster_create.dict())
        body = {"cluster": filtered_cluster_create.dict()}
        req = self.cluster_client.create(
            body=body,
            projectId=cluster_create.project_id,
            zone=cluster_create.zone,
        )
        res = req.execute()
        return dict(res)

    def get_gke_clusters(self, project_id: str, zone: str) -> List[dict]:
        req = self.cluster_client.list(zone=zone, projectId=project_id)
        res = req.execute()
        return dict(res)

    def describe_gke_cluster(
        self, zone: str, project_id: str, cluster_name: str
    ) -> dict:
        req = self.cluster_client.get(
            zone=zone, projectId=project_id, clusterId=cluster_name
        )
        res = req.execute()
        return dict(res)

    def update_gke_cluster(
        self,
        zone: str,
        project_id: str,
        cluster_name: str,
        cluster_update: GKEUpdate,
    ) -> dict:
        filtered_cluster_update = GKEUpdateAPIFilter(**cluster_update.dict())
        body = {"name": cluster_name, "update": filtered_cluster_update.dict()}
        req = self.cluster_client.update(
            zone=zone,
            projectId=project_id,
            clusterId=cluster_name,
            cluster=body,
        )
        res = req.execute()
        return dict(res)

    def delete_gke_cluster(
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
