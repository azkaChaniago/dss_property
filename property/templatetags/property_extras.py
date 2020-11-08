from babel.numbers import format_currency
from django import template

register = template.Library()

@register.simple_tag()
def calculate_area(length, width, *args, **kwargs):
    return f"{length * width}m\u00b2"

@register.simple_tag()
def calculate_price(price, *args, **kwargs):
    return f"{round(price / 1000000, 2)}Juta"

@register.simple_tag()
def set_currency(currency, locale, nominal, *args, **kwargs):
    return format_currency(nominal, currency, locale=locale)