#!/usr/bin/env bash

docker kill store_online | true && docker rm store_online | true
docker build -t store_online .
docker run -d --name store_online -p 8080:8080 store_online

# Создание суперпользователя Django
docker exec -ti store_online python3 /app/manage.py shell \
-c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@test.com', 'admin')"
