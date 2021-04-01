#!/bin/sh -ex

./scripts/lint.sh

pytest --cov=astrobase --cov=tests --cov-report=term-missing --cov-report=xml tests ${@}
