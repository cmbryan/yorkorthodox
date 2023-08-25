#!/bin/bash

SITE=./www

pip3 install --user -r requirements.txt
mkdir -p $SITE
python3 -m http.server -d $SITE &
while true; do
    python -m staticjinja watch --static static --outpath $SITE
    sleep 1
done