#!/usr/bin/env bash

python -m mkdocs build

cp ./docs/index.md ./README.md

git add README.md && git commit -S -m "Updated README.md from docs-build.sh"
