![YAMdb workflow](https://github.
com/koshelevd/foodgram-project/actions/workflows/main.yml/badge.svg)
# Foodgram project

Foodgram is a project about cooking, recipes and delicious food 

## Table of contents

- [Installing](#installing)
- [Build containers for project](#build-containers-for-project)
- [Create superuser](#create-superuser)
- [Load initial data to database](#load-initial-data-to-database)

## Installing
You have to install [Docker Desktop](https://www.docker.com/) in order to run application.

## Build containers for project:
```
$ docker-compose up
```

## Create superuser
```
$ docker-compose exec web python manage.py createsuperuser
```

## Load initial data to database
```
$ docker-compose run web python manage.py shell
>>> from django.contrib.contenttypes.models import ContentType
>>> ContentType.objects.all().delete()
>>> quit()
$ docker-compose run web python manage.py loaddata fixtures/fixtures.json
```

## Visit deployed project: 
http://fixtures.koshelev.net