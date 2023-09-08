#!/bin/sh

cd calendar
./_build.sh
cd ../scripts
./generate_service_db.py
