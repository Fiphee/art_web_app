import json
from django.core.management import BaseCommand
from art_web_app.settings import MEDIA_ROOT
from artworks.models import Artwork, Category
from users.models import AuthUserModel
from django.db import transaction
import random
import os
from PIL import Image
from utils.constants import THUMB_SIZE
import uuid


class Command(BaseCommand):
    
    help = 'Creates artworks'

    def add_arguments(self, parser):
        parser.add_argument('--folder', '-f', type=str)


    def _make_and_get_thumbnail(self, image, name, extension):
        img = Image.open(image)
        img.thumbnail(THUMB_SIZE, Image.ANTIALIAS)
        thumbnails_path = os.path.join(MEDIA_ROOT, 'artworks', 'thumbnails')

        thumb_filename = name + '_thumb.' + extension
        img.save(os.path.join(thumbnails_path, thumb_filename))
        img.close()
        return os.path.join('artworks', 'thumbnails', thumb_filename)


    def handle(self, *args, **options):
        directory = options.get('folder')
        users = AuthUserModel.objects.all()  
        artworks_path = os.path.join(MEDIA_ROOT, 'artworks', 'original_images')
        artworks = []
        art_count = 0
        folder_files = os.listdir(directory)
        for filename in folder_files:
            img = {}
            title , extension = filename.rsplit('.', 1)
            name = str(uuid.uuid4())

            extension = extension.lower()
            file_path = os.path.join(directory, filename)
            if extension in ['jpg', 'jpeg', 'png']:
                
                img['uploader'] = random.choice(users).username
                img['title'] = title
                img['description'] = 'No description'
                img['image'] = os.path.join('artworks', 'original_images', f'{name}.{extension}')
                
                current_image = Image.open(file_path)
                current_image.save(os.path.join(artworks_path, f'{name}.{extension}'), 'PNG')               
                current_image.close()

                # img['thumbnail'] = self._make_and_get_thumbnail(file_path, name, extension)

            artworks.append(img)
            art_count += 1
            print(f'{art_count} of {len(folder_files)} artworks created')
            
        save_json_to = os.path.join('data', 'artworks.json')
        with open(save_json_to, 'w') as f:
            json_data = json.dumps(artworks, indent=4)
            f.write(json_data)
        
        print(f'Created {art_count} artworks. Use "add_artworks" command to add them to the database.')
