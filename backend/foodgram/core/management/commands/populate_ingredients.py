import csv

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from psycopg2 import IntegrityError
from recipes.models import Ingredient, Unit


class Command(BaseCommand):
    help = 'Populates Ingredient model with given csv data'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str,
                            help='gives ')

    def handle(*args, **kwargs):
        path = kwargs['path']
        print(path)
        with open(path) as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    unit, _ = Unit.objects.get_or_create(name=row[1])
                    _, created = Ingredient.objects.get_or_create(
                        name=row[0],
                        unit=unit
                    )
                    print(f'ingredient {row[0]} was added')
                except IntegrityError:
                    print(f'ingredient {row[0]} caused integrity error')

        print('Ingredients model was populated')
