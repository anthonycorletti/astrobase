from fastapi import APIRouter

router = APIRouter()
tags = ["workflow"]


@router.post("/workflow", tags=tags)
def create_workflow():
    pass


@router.get("/workflow", tags=tags)
def get_workflows():
    pass


@router.get("/workflow/{workflow_name}", tags=tags)
def get_workflow():
    pass


@router.patch("/workflow/{workflow_name}", tags=tags)
def update_workflow():
    pass


@router.delete("/workflow/{workflow_name}", tags=tags)
def delete_workflow():
    pass
