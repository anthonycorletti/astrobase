import logging

from astrobase import gunicorn_config
from astrobase.logger import logger


def test_default_gunicorn_config(client):
    assert gunicorn_config.bind == ":8787"
    assert gunicorn_config.worker_class == "uvicorn.workers.UvicornWorker"


def test_default_logger(client):
    assert logger.getEffectiveLevel() == logging.INFO
