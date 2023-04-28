#!/usr/bin/env bash


set -o errexit

pip install --upgrade pip
pip install -r app/requirements.txt

chmod a+x * 
chmod -R a+x app/*