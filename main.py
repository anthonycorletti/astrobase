import os

from fastapi import FastAPI

from astrobase import __version__ as version
from astrobase.routers import auth, cluster, health, service, workflow

api = FastAPI(title="Astrobase API Server", version=os.getenv("SHORT_SHA", version))

api.include_router(health.router)
api.include_router(auth.router)
api.include_router(cluster.router)
api.include_router(service.router)
api.include_router(workflow.router)
