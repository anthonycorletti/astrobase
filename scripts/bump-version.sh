#!/bin/sh -e

current_version=$(python -c "import astrobase; print(astrobase.__version__)")
echo "current version: $current_version"
read -p "new version: " new_version

sed -i '' -e "s/$current_version/$new_version/g" astrobase/__init__.py

