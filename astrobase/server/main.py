import os

from fastapi import FastAPI

from astrobase import __version__
from astrobase.server.routers import aks, eks, gke, health

os.environ["TZ"] = "UTC"
api = FastAPI(title="Astrobase API Server", version=__version__)

api.include_router(health.router)
api.include_router(gke.router)
api.include_router(eks.router)
api.include_router(aks.router)
