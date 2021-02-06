import os

from fastapi import FastAPI

from astrobase import __version__ as version
from astrobase.routers import auth, health, infra, service

api = FastAPI(title="Astrobase API Server", version=os.getenv("SHORT_SHA", version))

api.include_router(health.router)
api.include_router(auth.router)
api.include_router(infra.router)
api.include_router(service.router)
