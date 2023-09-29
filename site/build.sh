#!/bin/sh

rm -rf /app/www
staticjinja build --static static --outpath /app/www
