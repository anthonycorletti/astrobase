#!/bin/sh -ex

mypy astrobase
flake8 astrobase tests
black astrobase tests --check
isort astrobase tests scripts --check-only
