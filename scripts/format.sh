#!/bin/sh -ex

# Sort imports one per line, so autoflake can remove unused imports
isort --force-single-line-imports astrobase tests scripts

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place astrobase tests scripts --exclude=__init__.py
black astrobase tests scripts
isort astrobase tests scripts
