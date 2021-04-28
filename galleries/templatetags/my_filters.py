from django import template


register = template.Library()

@register.filter
def reverse(value):
    return reversed(value)