#!/bin/sh -e

# Run our API in a docker image
# Will pull latest if not built locally with ./scripts/docker-build.sh
# Can run in interactive mode with; MODE="-it"./scripts/docker-run.sh /bin/bash

REGISTRY_NAME="gcr.io"
GCP_PROJECT="${GCP_PROJECT:=astrobasecloud}"

IMAGE_NAME="${GCP_PROJECT}/astrobase"
IMAGE_VERSION=${IMAGE_VERSION:=latest}

MODE=${MODE:="-d"}

docker run ${MODE} -p 8787:8787 --name=astrobase "${REGISTRY_NAME}/${IMAGE_NAME}:${IMAGE_VERSION}" ${@}
