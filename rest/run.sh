#!/bin/sh

# Run the server on :5000, restarting on failure
# (Ctrl-C twice to exit)
while true; do
    FLASK_APP=yorkorthodox-rest python -m flask --debug run --host 0.0.0.0
    sleep 1
done
