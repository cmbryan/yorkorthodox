#!/bin/sh

# This is only needed by render, which isn't using ../Dockerfile, as it's restricted to the rest sub-folder
export SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
export PYTHONPATH=$SCRIPT_DIR/..
python -m pip install -r ${SCRIPT_DIR}/requirements.txt

cd calendar
./_build.sh

cd ../scripts
./generate_service_db.py
