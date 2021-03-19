import os

from fastapi import APIRouter

from astrobase import __version__ as version

router = APIRouter()
tags = ["health"]


@router.get("/healthcheck", tags=tags)
def healthcheck():
    return {
        "message": "We're on the air.",
        "apiVersion": os.getenv("SHORT_SHA", version),
    }
