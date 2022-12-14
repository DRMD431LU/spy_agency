#!/bin/bash

Collect static files
echo "static files"
python spy_agency/manage.py collectstatic --noinput

# Apply database migrations
echo "migrations"
python manage.py migrate spy_agency
python spy_agency/manage.py migrate

# load data
echo "load data"
python spy_agency/manage.py loaddata spy_agency
