import json
from django.core.management import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):
    """
    Очиащает данные моделей Product и Category;
    Заливает в них данные из фикстуры catalog_data.json
    """
    def handle(self, *args, **options):
        """Основной код"""
        Category.objects.all().delete()
        Product.objects.all().delete()

        category_objects = []
        pruduct_objects = []

        with open('catalog_data.json', 'r') as json_file:
            data = json.load(json_file)

        for object in data:
            if object['model'] == 'catalog.category':
                category_objects.append(
                    Category(**object['fields'])
                )
            elif object['model'] == 'catalog.product':
                pruduct_objects.append(
                    Product(**object['fields'])
                )

        Category.objects.bulk_create(category_objects)
        Product.objects.bulk_create(pruduct_objects)
