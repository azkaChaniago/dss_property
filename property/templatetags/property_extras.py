from babel.numbers import format_currency, format_decimal
from django import template

register = template.Library()

@register.simple_tag()
def calculate_area(length, width, *args, **kwargs):
    return f"{length * width}m\u00b2"

@register.simple_tag()
def calculate_price(price, *args, **kwargs):
    display_price = float(price) / 1000000
    units = "Juta"
    if display_price >= 1000:
        display_price = display_price / 1000
        units = "Miliar"
    elif display_price >= 1000000:
        display_price = display_price / 1000000
        units = "Triliun"
    return f"{round(display_price, 2)}{units}"

@register.simple_tag()
def set_currency(currency, locale, nominal, *args, **kwargs):
    return format_currency(nominal, currency, locale=locale)