import json
from typing import Any, Dict

from fastapi import HTTPException
from google.auth import exceptions as google_auth_exceptions
from googleapiclient import errors as google_api_client_errors
from googleapiclient.discovery import build

from astrobase.schemas.gke import (
    GKECreate,
    GKECreateAPI,
    GKECreateAPIFilter,
    GKEErrorResponse,
)
from astrobase.server.logger import logger


class GKEApi:
    def __init__(self) -> None:
        try:
            self.client = build("container", "v1beta1", cache_discovery=False)
            self.cluster_client = self.client.projects().zones().clusters()
        except google_auth_exceptions.DefaultCredentialsError as e:
            logger.error(
                "Missing credentials for GKEApi. "
                "Make sure you've set your "
                "GOOGLE_APPLICATION_CREDENTIALS environment variable.\n"
                f"Full exception:\n{e}"
            )

    def create(self, cluster_create: GKECreate) -> Dict:
        body = GKECreateAPI(cluster=GKECreateAPIFilter(**cluster_create.dict()))
        return self.make_create_request(
            project_id=cluster_create.project_id,
            location=cluster_create.location,
            body=body.dict(),
        )

    def make_create_request(self, project_id: str, location: str, body: Dict) -> Dict:
        req = self.cluster_client.create(projectId=project_id, zone=location, body=body)
        return self.handle_google_request(req)

    def get(self, project_id: str, location: str) -> Dict:
        return self.make_get_request(project_id=project_id, location=location)

    def make_get_request(self, project_id: str, location: str) -> Dict:
        req = self.cluster_client.list(projectId=project_id, zone=location)
        return self.handle_google_request(req)

    def describe(self, project_id: str, location: str, cluster_name: str) -> Dict:
        return self.make_describe_request(
            project_id=project_id,
            location=location,
            cluster_name=cluster_name,
        )

    def make_describe_request(
        self, project_id: str, location: str, cluster_name: str
    ) -> Dict:
        req = self.cluster_client.get(
            projectId=project_id, zone=location, clusterId=cluster_name
        )
        return self.handle_google_request(req)

    def delete(self, project_id: str, location: str, cluster_name: str) -> Dict:
        return self.make_delete_request(
            project_id=project_id,
            location=location,
            cluster_name=cluster_name,
        )

    def make_delete_request(
        self, project_id: str, location: str, cluster_name: str
    ) -> Dict:
        req = self.cluster_client.delete(
            projectId=project_id, zone=location, clusterId=cluster_name
        )
        return self.handle_google_request(req)

    def handle_google_request(self, req: Any) -> Dict:
        try:
            res = req.execute()
            return dict(res)
        except google_api_client_errors.HttpError as e:
            content = e.content.decode("utf8")
            logger.error(content)
            err = GKEErrorResponse(**json.loads(content))
            raise HTTPException(status_code=err.error.code, detail=err.error.message)
