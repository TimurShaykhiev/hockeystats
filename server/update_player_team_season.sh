#!/usr/bin/env bash

source ~/.profile
SRC_ROOT=${HOCKEYSTATS_ROOT}/server

source ${SRC_ROOT}/venv/bin/activate
python ${SRC_ROOT}/update_player_team_season.py
