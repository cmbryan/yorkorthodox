# YorkOrthodox REST Server

Providing lectionary and commemoration data according to the Antiochian Orthodox Archdiocese of Great Britain and Ireland,
and service information for the parish in York, England.

## Usage

See the `/help` endpoint (e.g. `https://yorkorthodox-rest-2.onrender.com/help`)
for usage information.

## Developer

This service can be run on `localhost:5000` using `run.sh`.

### Deployment

The production server is hosted on `https://yorkorthodox-rest-2.onrender.com`.
The render service will pick up any changes to the rest folder on the main branch, and re-deploy
automatically.
