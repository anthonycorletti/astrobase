#!/bin/sh -ex

bash ./scripts/lint.sh

pytest --cov=fastapi --cov=tests --cov-report=term-missing --cov-report=xml tests ${@}
