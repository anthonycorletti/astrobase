import logging
import os
import time


def create_logger() -> logging.Logger:
    tz = time.strftime("%z")
    logging.basicConfig(
        format=(
            f"[%(asctime)s.%(msecs)03d {tz}] "
            "[%(process)s] [%(pathname)s L%(lineno)d] "
            "[%(levelname)s] %(message)s"
        ),
        level=os.environ.get("LOGLEVEL", "INFO").upper(),
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger(__name__)
    return logger


logger = create_logger()
