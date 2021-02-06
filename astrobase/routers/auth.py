from fastapi import APIRouter

router = APIRouter()
tags = ["auth"]


@router.get("/auth", tags=tags)
def list_auth():
    pass


@router.post("/revoke", tags=tags)
def revoke_auth():
    pass
