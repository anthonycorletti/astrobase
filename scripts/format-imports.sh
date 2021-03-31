#!/bin/sh -ex

# Sort imports one per line, so autoflake can remove unused imports
isort main.py astrobase tests scripts --force-single-line-imports

sh ./scripts/format.sh
