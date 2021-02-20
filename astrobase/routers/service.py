from fastapi import APIRouter, Body

from astrobase.apis.service import ServiceAPI
from astrobase.schemas.service import KubernetesServiceCreate

services_api = ServiceAPI()
router = APIRouter()
tags = ["service"]


@router.post("/kubernetes/service", tags=tags)
def kubernetes_create_service(
    kubernetes_service_create: KubernetesServiceCreate = Body(...),
):
    return services_api.create_kubernetes_service(kubernetes_service_create)


@router.get("/kubernetes/service", tags=tags)
def kubernetes_get_services():
    pass


@router.get("/kubernetes/service/{service_name}", tags=tags)
def kubernetes_get_service():
    pass


@router.patch("/kubernetes/service/{service_name}", tags=tags)
def kubernetes_update_service():
    pass


@router.delete("/kubernetes/service/{service_name}", tags=tags)
def kubernetes_delete_service():
    pass
