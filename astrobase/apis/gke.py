import json
from typing import List

import googleapiclient
from googleapiclient.discovery import build

from astrobase.schemas.gke import GKECreate, GKECreateAPI, GKECreateFilter


class GKEApi:
    def __init__(self):
        self.client = build("container", "v1beta1")
        self.cluster_client = self.client.projects().locations().clusters()

    def create(self, cluster_create: GKECreate) -> dict:
        body = GKECreateAPI(cluster=GKECreateFilter(**cluster_create.dict()))
        req = self.cluster_client.create(parent=cluster_create.parent, body=body.dict())
        res = req.execute()
        return dict(res)

    def get(self, project_id: str, location: str) -> List[dict]:
        parent = f"projects/{project_id}/locations/{location}"
        req = self.cluster_client.list(parent=parent)
        res = req.execute()
        return dict(res)

    def describe(self, location: str, project_id: str, cluster_name: str) -> dict:
        name = f"projects/{project_id}/locations/{location}/clusters/{cluster_name}"
        req = self.cluster_client.get(name=name)
        try:
            res = req.execute()
            return dict(res)
        except googleapiclient.errors.HttpError as e:
            content = e.content.decode("utf8")
            return json.loads(content)

    def delete(self, location: str, project_id: str, cluster_name: str) -> dict:
        name = f"projects/{project_id}/locations/{location}/clusters/{cluster_name}"
        req = self.cluster_client.delete(name=name)
        try:
            res = req.execute()
            return dict(res)
        except googleapiclient.errors.HttpError as e:
            content = e.content.decode("utf8")
            return json.loads(content)
