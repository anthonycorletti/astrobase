#!/bin/sh -ex

pip install --upgrade pip
pip install flit
flit publish
