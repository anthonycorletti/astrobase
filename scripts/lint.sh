#!/bin/sh -ex

mypy astrobasecloud tests
flake8 astrobasecloud tests
black astrobasecloud tests --check
isort astrobasecloud tests scripts --check-only
