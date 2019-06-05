#!/usr/bin/env bash

python3 manage.py migrate --no-input
python3 manage.py makemigrations
python3 manage.py migrate --no-input
django-admin compilemessages
python3 manage.py runserver 0.0.0.0:8080
