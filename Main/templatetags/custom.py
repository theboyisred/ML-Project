from django import template

register = template.Library()

@register.filter
def lookup(d: dict, key):
    return d.get(key, None)