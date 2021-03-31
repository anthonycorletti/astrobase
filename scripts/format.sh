#!/bin/sh -ex

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place main.py astrobase tests scripts --exclude=__init__.py
black main.py astrobase tests scripts
isort main.py astrobase tests scripts
