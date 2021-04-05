FROM python:3.9.0-slim

WORKDIR /astrobase

COPY . /astrobase

RUN apt-get update -y \
    && apt-get install build-essential -y \
    && rm -rf /var/lib/apt/lists/* \
    && pip install flit \
    && FLIT_ROOT_INSTALL=1 flit install --deps=all --extras=all

CMD gunicorn astrobase.main:api -c astrobase/config/gunicorn.py
