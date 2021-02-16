#!/bin/bash

python uks_project/manage.py makemigrations
python uks_project/manage.py migrate
python uks_project/manage.py test users issues_app projects_app wiki_app
python uks_project/manage.py runserver 0.0.0.0:8000