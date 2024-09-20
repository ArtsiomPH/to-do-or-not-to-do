#!/bin/sh

echo "Collect static files."
poetry run python manage.py collectstatic --noinput

echo "Apply database migrations."
poetry run python manage.py migrate

echo "Creating superuser."
poetry run python manage.py init-admin

echo "Run server"
task run-server-dev