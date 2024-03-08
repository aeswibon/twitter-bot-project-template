#!/usr/bin/env sh
set -euo pipefail

printf "api" >> /tmp/container-role

cd /app

echo "starting server..."
python manage.py runserver 0.0.0.0:9000
