#!/bin/sh

SITE=/app/www

mkdir -p $SITE
python3 -m http.server -d $SITE &
while true; do
    staticjinja watch --srcpath /app/templates --outpath $SITE
    sleep 1
done
