import os

from fastapi import FastAPI

from astrobase import __version__ as version
from astrobase.routers import gke, health, workflow

api = FastAPI(title="Astrobase API Server", version=os.getenv("SHORT_SHA", version))

api.include_router(health.router)
api.include_router(gke.router)
api.include_router(workflow.router)
