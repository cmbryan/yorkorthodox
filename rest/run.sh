#!/bin/bash

pip3 install -r requirements.txt
while true; do
    FLASK_APP=hellofly python -m flask run --host 0.0.0.0
    sleep 1
done
