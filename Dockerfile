FROM python:3.9.7-slim

WORKDIR /astrobase

COPY . /astrobase

RUN apt-get update -y \
    && rm -rf /var/lib/apt/lists/* \
    && pip install flit \
    && FLIT_ROOT_INSTALL=1 flit install --deps=production --extras=all

CMD gunicorn astrobase.server.main:api -c astrobase/server/gunicorn_config.py
