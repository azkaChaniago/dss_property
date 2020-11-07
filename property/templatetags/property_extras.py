from django import template

register = template.Library()

@register.simple_tag()
def calculate_area(length, width, *args, **kwargs):
    return f"{length * width}m\u00b2"