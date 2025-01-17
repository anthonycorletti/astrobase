#!/bin/sh -ex

./scripts/format.sh

./scripts/lint.sh

pytest --cov=astrobasecloud --cov=tests --cov-report=term-missing --cov-report=xml -o console_output_style=progress --disable-warnings --cov-fail-under=100 ${@}
