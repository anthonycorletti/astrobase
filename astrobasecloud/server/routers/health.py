from datetime import datetime

from fastapi import APIRouter

from astrobasecloud import __version__
from astrobasecloud.server.logger import logger
from astrobasecloud.types.health import HealthcheckResponse

router = APIRouter(tags=["health"])


@router.get("/healthcheck", response_model=HealthcheckResponse)
def healthcheck() -> HealthcheckResponse:
    message = "We're on the air."
    logger.info(message)
    return HealthcheckResponse(
        version=__version__, message=message, time=datetime.now()
    )
