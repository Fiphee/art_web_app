from django.core.management.base import BaseCommand
from artworks.models import Category


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        categories = Category.objects.filter(name__icontains='rgb(')
        n = 0
        for category in categories:
            n += 1
            category.delete()
            print(f'Removed {n} color categories out of {len(categories)}')