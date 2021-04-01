import os
from datetime import datetime

from fastapi import APIRouter

from astrobase import __version__ as version
from astrobase.config.logger import logger

router = APIRouter()
tags = ["health"]


@router.get("/healthcheck", tags=tags)
def healthcheck():
    message = "We're on the air."
    logger.info(message)
    return {
        "message": message,
        "time": str(datetime.now()),
        "apiVersion": os.getenv("SHORT_SHA", version),
    }
