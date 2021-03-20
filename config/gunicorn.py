import os

threads = 2
workers = 3
timeout = 60
bind = f":{os.getenv('ASTROBASE_HOST_PORT', '8787')}"
worker_class = "uvicorn.workers.UvicornWorker"
