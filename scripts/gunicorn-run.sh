#!/bin/sh -e

gunicorn astrobase.server.main:api -c astrobase/server/gunicorn_config.py
