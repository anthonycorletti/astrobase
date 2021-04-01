FROM python:3.9.0-slim

WORKDIR /astrobase

COPY . /astrobase

RUN apt-get update -y \
    && apt-get install build-essential -y \
    && rm -rf /var/lib/apt/lists/* \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-dev

CMD gunicorn astrobase.main:api -c astrobase/config/gunicorn.py
