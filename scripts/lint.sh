#!/bin/sh -ex

mypy main.py astrobase
flake8 main.py astrobase tests
black main.py astrobase tests --check
isort main.py astrobase tests scripts --check-only
