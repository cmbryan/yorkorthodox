#!/bin/sh

# Run the server on :5000, restarting on failure
# (Ctrl-C twice to exit)
while true; do
    gunicorn -b 127.0.0.1:5000 yorkorthodox-rest:app
    sleep 1
done
