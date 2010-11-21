from ..api import narrow_buttons, wide_buttons
from django import template

register = template.Library()

@register.simple_tag
def wide_social_buttons(request, title, url):
    return wide_buttons(request, title, url)

@register.simple_tag
def narrow_social_buttons(request, title, url):
    return narrow_buttons(request, title, url)
