import logging

from astrobase.config import gunicorn
from astrobase.config.logger import logger


def test_default_gunicorn_config(client):
    assert gunicorn.bind == ":8787"
    assert gunicorn.worker_class == "uvicorn.workers.UvicornWorker"


def test_default_logger(client):
    assert logger.getEffectiveLevel() == logging.INFO
