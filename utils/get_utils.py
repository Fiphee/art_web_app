from galleries.models import GalleryArtwork


def get_next_position(instance):
    try:
        next_position = GalleryArtwork.objects.filter(gallery_id=instance.id).order_by('-position').first().position + 1
    except AttributeError:
        next_position = 1
    
    return next_position