#!/bin/sh -e

gunicorn astrobasecloud.server.main:api -c astrobasecloud/server/gunicorn_config.py
