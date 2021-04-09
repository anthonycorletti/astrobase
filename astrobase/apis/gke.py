import json
from typing import Any, Optional

from fastapi import HTTPException
from google.auth import exceptions as google_auth_exceptions
from googleapiclient import errors as google_api_client_errors
from googleapiclient.discovery import build

from astrobase.config.logger import logger
from astrobase.schemas.gke import (
    GKECreate,
    GKECreateAPI,
    GKECreateAPIFilter,
    GKEErrorResponse,
)


class GKEApi:
    def __init__(self):
        try:
            self.client = build("container", "v1beta1")
            self.cluster_client = self.client.projects().zones().clusters()
        except google_auth_exceptions.DefaultCredentialsError as e:
            logger.error(
                "Missing credentials for GKEApi. "
                "Make sure you've set your "
                "GOOGLE_APPLICATION_CREDENTIALS environment variable.\n"
                f"Full exception:\n{e}"
            )

    def create(self, cluster_create: GKECreate) -> dict:
        logger.info(f"cluster_create {cluster_create.dict()}")
        body = GKECreateAPI(cluster=GKECreateAPIFilter(**cluster_create.dict()))
        return self.make_create_request(parent=cluster_create.parent, body=body.dict())

    def make_create_request(self, parent: Optional[str], body: dict) -> dict:
        req = self.cluster_client.create(parent=parent, body=body)
        return self.handle_google_request(req)

    def get(self, project_id: str, location: str) -> dict:
        return self.make_get_request(f"projects/{project_id}/zones/{location}")

    def make_get_request(self, parent: str) -> dict:
        req = self.cluster_client.list(parent=parent)
        return self.handle_google_request(req)

    def describe(self, location: str, project_id: str, cluster_name: str) -> dict:
        return self.make_describe_request(
            f"projects/{project_id}/zones/{location}/clusters/{cluster_name}"
        )

    def make_describe_request(self, name: str) -> dict:
        req = self.cluster_client.get(name=name)
        return self.handle_google_request(req)

    def delete(self, location: str, project_id: str, cluster_name: str) -> dict:
        return self.make_delete_request(
            f"projects/{project_id}/zones/{location}/clusters/{cluster_name}"
        )

    def make_delete_request(self, name: str) -> dict:
        req = self.cluster_client.delete(name=name)
        return self.handle_google_request(req)

    def handle_google_request(self, req: Any) -> dict:
        try:
            res = req.execute()
            return dict(res)
        except google_api_client_errors.HttpError as e:
            content = e.content.decode("utf8")
            logger.error(content)
            err = GKEErrorResponse(**json.loads(content))
            raise HTTPException(status_code=err.error.code, detail=err.error.message)
