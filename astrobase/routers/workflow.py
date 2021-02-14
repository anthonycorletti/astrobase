from fastapi import APIRouter

router = APIRouter()
tags = ["workflow"]


@router.post("/workflow", tags=tags)
def create_workflow():
    pass


@router.get("/workflow", tags=tags)
def get_workflow():
    pass


@router.patch("/workflow", tags=tags)
def update_workflow():
    pass


@router.delete("/workflow", tags=tags)
def delete_workflow():
    pass
