import csv

from django.core.management.base import BaseCommand
from recipes.models import Tag


class Command(BaseCommand):
    help = 'Populates Tag model with given csv data'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str,
                            help='path to cvs-file containing tags')

    def handle(*args, **kwargs):
        path = kwargs['path']
        print(path)
        with open(path) as file:
            reader = csv.reader(file)
            for row in reader:
                Tag.objects.get_or_create(name=row[0],
                                          slug=row[1], hex_code=row[2])

        print('Tag model was populated')
