#!/bin/sh -ex

# Sort imports one per line, so autoflake can remove unused imports
isort --force-single-line-imports astrobasecloud tests scripts

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place astrobasecloud tests scripts --exclude=__init__.py
black astrobasecloud tests scripts
isort astrobasecloud tests scripts
