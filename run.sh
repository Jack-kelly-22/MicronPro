#!/bin/bash

NO_RELOAD=""

if [[ $# -lt 1 || $# -gt 2 ]]; then
    echo "use: ./run.sh {app.py} [-r]"
    exit 1
fi

if [[ $# -eq 2 && $2 == "-r" ]]; then
    NO_RELOAD="--no-reload"
fi

echo "Application is going live"
export FLASK_APP=$1
export FLASK_ENV=development
flask run $NO_RELOAD

