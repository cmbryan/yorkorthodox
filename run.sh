#!/bin/sh

# Run development versions of both the website and the REST server

cd site; sh ./run.sh &
cd ../rest; sh ./run.sh
