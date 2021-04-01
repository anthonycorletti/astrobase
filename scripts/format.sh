#!/bin/sh -ex

# Sort imports one per line, so autoflake can remove unused imports
isort --force-single-line-imports main.py astrobase tests scripts

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place main.py astrobase tests scripts --exclude=__init__.py
black main.py astrobase tests scripts
isort main.py astrobase tests scripts
