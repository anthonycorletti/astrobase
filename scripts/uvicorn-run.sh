#!/bin/sh -e

uvicorn astrobase.server.main:api --reload ${@}
