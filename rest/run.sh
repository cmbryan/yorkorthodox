#!/bin/sh

if [ -z $DEBUG ]; then
    gunicorn -b 0.0.0.0:5000 app.yorkorthodox_rest:app
else
    while true; do
        python /workspace/rest/app/yorkorthodox_rest.py
        sleep 1
    done
fi
