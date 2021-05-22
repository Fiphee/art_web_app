from colorthief import ColorThief
from .constants import COLOR_THRESHOLD
from math import sqrt 
import os


def get_colors(art):
    getcolors = ColorThief(art)
    palette = getcolors.get_palette(color_count=30)
    palette = (palette[0],palette[1],palette[2],palette[3],palette[4],palette[-1])
    return palette


def get_best_category(color, similar_colors):
    smallest_difference = COLOR_THRESHOLD
    selected_color_category = None
    r,g,b = color
    for db_color in similar_colors:
        color_difference = sqrt(abs(r-db_color.r)**2 + abs(g-db_color.g)**2 + abs(b-db_color.b)**2)
        if color_difference < smallest_difference:
            smallest_difference = color_difference
            selected_color_category = db_color.category
    return selected_color_category
    