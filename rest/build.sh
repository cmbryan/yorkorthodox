#!/bin/sh

set -e

cd calendar
./_build.sh

cd ../scripts
./generate_service_db.py
