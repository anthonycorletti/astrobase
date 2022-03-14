import logging

from fastapi.testclient import TestClient

from astrobasecloud.server import gunicorn_config
from astrobasecloud.server.logger import logger


def test_default_gunicorn_config(client: TestClient) -> None:
    assert gunicorn_config.bind == ":8787"
    assert gunicorn_config.worker_class == "uvicorn.workers.UvicornWorker"


def test_default_logger(client: TestClient) -> None:
    assert logger.getEffectiveLevel() == logging.INFO
