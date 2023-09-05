#!/bin/sh

pip install -r requirements.txt

cd scripts
./generate_service_db.py
