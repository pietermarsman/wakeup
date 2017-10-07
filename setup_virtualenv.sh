#!/bin/bash

rm -r .venv

virtualenv -p python3 .venv

source .venv/bin/activate
pip install -r app/requirements.txt
deactivate