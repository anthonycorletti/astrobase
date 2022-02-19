import os
from datetime import datetime

from fastapi import APIRouter

from astrobase import __version__
from astrobase.server.logger import logger

router = APIRouter()


@router.get("/healthcheck", tags=["health"])
def healthcheck() -> dict:
    message = "We're on the air."
    logger.info(message)
    return {
        "version": os.getenv("SHORT_SHA", __version__),
        "message": message,
        "time": str(datetime.now()),
    }
