import os

from fastapi import APIRouter

from astrobase import __version__ as version

router = APIRouter()
tags = ["health"]


@router.get("/healthcheck", tags=tags)
def healthcheck():
    """
    going to the doctor
    """
    return {
        "message": "alive and kicking",
        "version": os.getenv("SHORT_SHA", version),
    }
