from fastapi import APIRouter

router = APIRouter()
tags = ["service"]


@router.post("/service", tags=tags)
def create_service():
    pass


@router.get("/service", tags=tags)
def get_service():
    pass


@router.patch("/service", tags=tags)
def update_service():
    pass


@router.delete("/service", tags=tags)
def delete_service():
    pass
