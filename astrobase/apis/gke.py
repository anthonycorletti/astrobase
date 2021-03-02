import json
from typing import List

import googleapiclient
from googleapiclient.discovery import build
from kubernetes import client

from astrobase.schemas.gke import (
    GKECreate,
    GKECreateAPI,
    GKECreateFilter,
    GKEResourceCreate,
)


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

    def create_resource(
        self,
        cluster_name: str,
        project_id: str,
        location: str,
        gke_resource_create: GKEResourceCreate,
    ) -> dict:
        print(f"creating resource: {gke_resource_create}")
        cluster = self.describe(
            location=location,
            project_id=project_id,
            cluster_name=cluster_name,
        )
        cluster_endpoint = cluster.get("endpoint")
        ssl_ca_cert = cluster.get("masterAuth", {}).get("clusterCaCertificate")
        kubeconf = client.Configuration(host=f"https://{cluster_endpoint}")
        kubeconf.verify_ssl = True
        kubeconf.ssl_ca_cert = ssl_ca_cert
        print("kubeconf, ", kubeconf)
        # hm, what to do here, kubectl is really functional
        # could be a pain in the ass working in api calls ...
        # shell out from the cli to kubectl?
        # will have to get the right kubeconfig data to that call ...
        # how to do on the server side???
