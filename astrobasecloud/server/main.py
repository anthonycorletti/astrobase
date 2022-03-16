import os

from fastapi import FastAPI

from astrobasecloud import __version__
from astrobasecloud.server.routers import aws, azure, gcp, health

os.environ["TZ"] = "UTC"
api = FastAPI(title="Astrobase API Server", version=__version__)

api.include_router(health.router)
api.include_router(gcp.router)
api.include_router(aws.router)
api.include_router(azure.router)
