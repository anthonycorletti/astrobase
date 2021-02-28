from fastapi import APIRouter, Body

from astrobase.apis.kubernetes import KubernetesAPI
from astrobase.schemas.resource import KubernetesResourceCreate

kubernetes_api = KubernetesAPI()
router = APIRouter()
tags = ["resource"]


@router.post("/kubernetes/resource", tags=tags)
def kubernetes_create_resource(
    kubernetes_resource_create: KubernetesResourceCreate = Body(...),
):
    return kubernetes_api.create_kubernetes_resource(kubernetes_resource_create)


@router.get("/kubernetes/resource", tags=tags)
def kubernetes_get_resources():
    pass


@router.get("/kubernetes/resource/{resource_name}", tags=tags)
def kubernetes_get_resource():
    pass


@router.put("/kubernetes/resource/{resource_name}", tags=tags)
def kubernetes_update_resource():
    pass


@router.delete("/kubernetes/resource/{resource_name}", tags=tags)
def kubernetes_delete_resource():
    pass
