from django import template


register = template.Library()

@register.filter
def convert_symbols(category):
    safe_category = category.name.replace('&', '%26')
    return safe_category