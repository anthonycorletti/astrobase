import logging
import time


def create_logger(level: int = logging.INFO) -> logging.Logger:
    tz = time.strftime("%z")
    logging.config = logging.basicConfig(
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


logger = create_logger()
