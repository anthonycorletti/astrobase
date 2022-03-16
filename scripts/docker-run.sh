#!/bin/sh -e

# Run Astrobase in a docker container
# This script pulls the latest build if not built locally with ./scripts/docker-build.sh

REGISTRY_NAME="gcr.io"
GCP_PROJECT="${GCP_PROJECT:=astrobasecloud}"

IMAGE_NAME="${GCP_PROJECT}/astrobase"
IMAGE_VERSION=${IMAGE_VERSION:=latest}

docker run -p 8787:8787 --rm --name=astrobase "${REGISTRY_NAME}/${IMAGE_NAME}:${IMAGE_VERSION}" ${@}
