import os
from datetime import datetime

from fastapi import APIRouter

from astrobase import __version__ as version
from astrobase import api_version
from astrobase.config.logger import logger

router = APIRouter()
tags = ["health"]


@router.get("/healthcheck", tags=tags)
def healthcheck() -> dict:
    message = "We're on the air."
    logger.info(message)
    return {
        "api_version": api_version,
        "api_release_version": os.getenv("SHORT_SHA", version),
        "message": message,
        "time": str(datetime.now()),
    }
