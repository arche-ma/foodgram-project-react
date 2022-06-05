#!/bin/sh
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py populate_ingredients data/ingredients.csv
python3 manage.py populate_tags data/tags.csv
python3 manage.py collectstatic
python3 manage.py createsuperuser