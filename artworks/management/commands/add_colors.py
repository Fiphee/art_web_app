from django.core.management.base import BaseCommand
from artworks.models import Artwork, Color, Category
from utils.colors import get_colors, get_best_category
from utils.constants import COLOR_THRESHOLD
import colorthief


class Command(BaseCommand):
    def handle(self, *args, **options):
        artworks = Artwork.objects.filter(colors=None)
        n = 0
        for art in artworks:
            color_palette = get_colors(art.image.path) 
            
            create_category = lambda r,g,b: Category.objects.create(name=f'rgb({r}, {g}, {b})')
            
            for color in color_palette:
                r,g,b = color
                threshold = COLOR_THRESHOLD
                find_similar_args = {
                    'r__lte':r+threshold,
                    'r__gte':r-threshold,
                    'g__lte':g+threshold,
                    'g__gte':g-threshold,
                    'b__lte':b+threshold,
                    'b__gte':b-threshold,
                }
                
                try:  # if color exists then get its category
                    color_obj = Color.objects.get(r=r,g=g,b=b)
                    art.colors.add(color_obj)
                except Color.DoesNotExist:
                    similar_colors = Color.objects.filter(**find_similar_args)
                    if similar_colors.exists():  # check if similar colors have fitting categories
                        category = get_best_category(color, similar_colors)
                        if not category:
                            category = create_category(r,g,b)

                        current_color = Color.objects.create(r=r,g=g,b=b, category=category)
                    else: 
                        category = create_category(r,g,b)
                        current_color = Color.objects.create(r=r,g=g,b=b, category=category)

                    art.colors.add(current_color)
            n += 1
            print(f'{n} artworks out of {len(artworks)} completed!')
            
        print(f'Added colors to {n} artworks!')