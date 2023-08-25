#!/bin/bash

# Python requirements
pip3 install -r requirements.txt

# Fly hosting CLI
apt update && apt install -y curl
curl -L https://fly.io/install.sh | sh
echo export PATH="/root/.fly/bin:$PATH" >> ~/.bashrc

# Run the server on :5000, restarting on failure
# (Ctrl-C twice to exit)
while true; do
    FLASK_APP=hellofly python -m flask run --host 0.0.0.0
    sleep 1
done
