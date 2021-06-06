from django import template


register = template.Library()


@register.filter
def remove_last_parameters(url):
    split_url = url.split('&')
    if len(split_url) == 2:
        split_url.pop()
    elif len(split_url) > 2:
        split_url.pop()
        split_url.pop()
    return '&'.join(split_url)