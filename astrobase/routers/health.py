import os

from fastapi import APIRouter

from astrobase import __version__ as version

router = APIRouter()
tags = ["health"]


@router.get("/healthcheck", tags=tags)
def healthcheck():
    return {
        "message": "healthy",
        "version": os.getenv("SHORT_SHA", version),
    }
