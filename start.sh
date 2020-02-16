#!/usr/bin/env bash
BASEDIR=$(dirname "$0")
cd "$BASEDIR" || exit
source venv/bin/activate
export MUSIC_LIBRARY_PATHS="/home/panos/Music" # add more seperated with ','
python3 music_library.py
