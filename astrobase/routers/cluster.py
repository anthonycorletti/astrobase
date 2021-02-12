from fastapi import APIRouter

router = APIRouter()
tags = ["cluster"]


@router.post("/cluster", tags=tags)
def create_cluster():
    pass


@router.get("/cluster", tags=tags)
def get_cluster():
    pass


@router.patch("/cluster", tags=tags)
def update_cluster():
    pass


@router.delete("/cluster", tags=tags)
def delete_cluster():
    pass
