from typing import List

from fastapi import APIRouter, Body, Depends

from astrobase.apis.auth import AuthAPI
from astrobase.schemas.auth import AstroToken
from astrobase.schemas.cluster import Cluster, ClusterCreate, ClusterUpdate
from tests.factories import ClusterFactory

auth_api = AuthAPI()
router = APIRouter()
tags = ["cluster"]


@router.post("/cluster", tags=tags, response_model=Cluster)
def create_cluster(
    astro_token: AstroToken = Depends(auth_api.astro_client),
    cluster: ClusterCreate = Body(..., example=ClusterFactory.google_example),
):
    return {"cluster": cluster, "astro_token": astro_token}


@router.get("/cluster", tags=tags, response_model=List[Cluster])
def get_clusters(astro_token: AstroToken):
    pass


@router.get("/cluster/{cluster_name}", tags=tags, response_model=Cluster)
def describe_cluster(cluster_name: str, astro_token: AstroToken):
    pass


@router.patch("/cluster", tags=tags, response_model=Cluster)
def update_cluster(cluster_name: str, cluster: ClusterUpdate, astro_token: AstroToken):
    pass


@router.delete("/cluster", tags=tags)
def delete_cluster(cluster_name: str, astro_token: AstroToken):
    pass
