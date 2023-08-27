#!/bin/sh

# Run the server on :5000, restarting on failure
# (Ctrl-C twice to exit)
while true; do
    FLASK_APP=hellofly python -m flask run --host 0.0.0.0
    sleep 1
done
