from fastapi import APIRouter

router = APIRouter()
tags = ["infra"]


@router.post("/infra", tags=tags)
def create_infra():
    pass


@router.get("/infra", tags=tags)
def get_infra():
    pass


@router.patch("/infra", tags=tags)
def update_infra():
    pass


@router.delete("/infra", tags=tags)
def delete_infra():
    pass
