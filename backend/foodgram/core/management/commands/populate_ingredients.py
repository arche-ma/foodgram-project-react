import csv
from recipes.models import Ingredient, Unit
from django.core.management.base import BaseCommand


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
                unit, _ = Unit.objects.get_or_create(name=row[1])
                _, created = Ingredient.objects.get_or_create(
                    name=row[0],
                    unit=unit
                )
        print('Ingredients model was populated')
