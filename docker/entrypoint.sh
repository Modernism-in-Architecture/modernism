#!/bin/bash

set -e

python app/manage.py migrate --noinput

python app/manage.py collectstatic --noinput

exec "$@"
