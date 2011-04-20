from django.conf import settings
from django.template import Library

GOOGLE_CUSTOM_SEARCH_ID = getattr(settings, 'GOOGLE_CUSTOM_SEARCH_ID', None)

register = Library()

@register.inclusion_tag('google_cse/form.html')
def google_search_form(cse_id=GOOGLE_CUSTOM_SEARCH_ID):
    return {'google_custom_search_id': cse_id}
