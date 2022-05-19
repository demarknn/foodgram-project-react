import csv
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Load ingredients from csv'

    def handle(self, *args, **options):
        with open('data/ingredients.csv', encoding='utf-8') as f:
            file_reader = csv.reader(f)
            for row in file_reader:
                name, measurement_unit = row
                Ingredient.objects.get_or_create(
                    name=name, measurement_unit=measurement_unit)
