import logging
import os
import time

ASTROBASE_DEBUG = os.environ.get("ASTROBASE_DEBUG") == "true"


def create_logger(level: int = logging.INFO) -> logging.Logger:
    tz = time.strftime("%z")
    logging.basicConfig(
        format=(
            f"[%(asctime)s.%(msecs)03d {tz}] "
            "[%(process)s] [%(pathname)s L%(lineno)d] "
            "[%(levelname)s] %(message)s"
        ),
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger(__name__)
    return logger


if ASTROBASE_DEBUG:
    logger = create_logger(level=logging.DEBUG)
else:
    logger = create_logger()
