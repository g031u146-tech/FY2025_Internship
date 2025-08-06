#!/usr/bin/bash

venvPath='./venv/20250805/bin/activate'

source $venvPath
python ./Component/exec_server.py
deactivate
