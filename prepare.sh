#!/bin/sh

python manage.py collectstatic --noinput
python manage.py makemigrations users
python manage.py migrate users
python manage.py makemigrations about
python manage.py migrate about
python manage.py makemigrations api
python manage.py migrate api
python manage.py makemigrations recipes
python manage.py migrate recipes
python manage.py makemigrations
python manage.py migrate

exec "$@"