#!/bin/sh

if [ -z DEBUG ]; then
    ROOT=/app
else
    ROOT=/workspace/site
fi
SITE=${ROOT}/www

mkdir -p $SITE
python3 -m http.server -d $SITE &
while true; do
    python -m staticjinja watch --src-dir ${ROOT}/templates --outpath $SITE
    sleep 1
done
