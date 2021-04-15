import os

from fastapi import FastAPI

from astrobase import __version__ as version
from astrobase.routers import aks, eks, gke, health

os.environ["TZ"] = "UTC"
api = FastAPI(title="Astrobase API Server", version=os.getenv("SHORT_SHA", version))

api.include_router(health.router)
api.include_router(gke.router)
api.include_router(eks.router)
api.include_router(aks.router)
