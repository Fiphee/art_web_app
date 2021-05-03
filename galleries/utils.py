def get_next_position(model, **kwargs):
    try:
        next_position = model.objects.filter(**kwargs).order_by('-position').first().position + 1
    except AttributeError:
        next_position = 1
    
    return next_position
