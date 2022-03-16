#!/bin/sh -e

uvicorn astrobasecloud.server.main:api --reload ${@}
