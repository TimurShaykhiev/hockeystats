#! /bin/bash

VIRTUAL_ENV=/home/timur/venv/hockstat
SCHEDULER_ROOT=/home/timur/sources/hockeystats

source ${VIRTUAL_ENV}/bin/activate
python ${SCHEDULER_ROOT}/scheduler.py
