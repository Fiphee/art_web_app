from django import template
from utils.constants import ART_LIKE, FOLLOW, COMMENT, COMMENT_LIKE, GALLERY_LIKE, GALLERY_FOLLOW, REPLY


register = template.Library()

@register.filter
def total(activity, count):
    texts = {
        ART_LIKE: f'You have {count} new Art likes!',
        FOLLOW: f'You have {count} new Followers!',
        COMMENT: f'You have {count} new Comments!',
        COMMENT_LIKE: f'You have {count} new Comment likes!',
        GALLERY_LIKE: f'You have {count} new Gallery likes!',
        GALLERY_FOLLOW: f'You have {count} new Gallery followers!',
        REPLY: f'You have {count} new Comment replies!',
    }

    return texts[activity]

