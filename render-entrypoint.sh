#!/bin/sh
set -o errexit
set -o pipefail

python manage.py migrate --noinput
python manage.py collectstatic --noinput

gunicorn memorygame.wsgi:application --bind 0.0.0.0:8000
