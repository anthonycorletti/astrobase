#!/bin/sh -ex

mypy astrobase tests
flake8 astrobase tests
black astrobase tests --check
isort astrobase tests scripts --check-only
