import os

bind = f":{os.environ.get('PORT', '8787')}"
threads = 2
workers = 3
timeout = 60
worker_class = "uvicorn.workers.UvicornWorker"
