from django.core.management import BaseCommand
from artworks.models import Artwork, Category
from users.models import AuthUserModel
from django.db import transaction
import random
import os
import json


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = ['portrait','landscape','traditional', 'colorful', 'master']

        with open(os.path.join('data', 'artworks.json')) as f:
            json_data = json.load(f)

        try:
            art_count = 0
            with transaction.atomic():
                for art in json_data:
                    user = AuthUserModel.objects.filter(username=art['uploader']).first()
                    category_choice = random.choice(categories)
                    
                    db_category = Category.objects.filter(name=category_choice).first()
                    if not db_category:
                        db_category = Category(name=category_choice).save()

                    artwork = Artwork.objects.create(
                        uploader=user, 
                        title=art['title'],
                        description=art['description'],
                        image=art['image'],
                        thumbnail=art['thumbnail'],
                    )
                    artwork.category.add(db_category)
                    artwork.save()
                    art_count += 1
                print(f'Added {art_count} artworks!')
        except Exception as e:
            print(e)
