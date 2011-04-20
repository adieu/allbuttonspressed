from django.conf import settings
from django.template import Library

GOOGLE_ANALYTICS_ID = getattr(settings, 'GOOGLE_ANALYTICS_ID', None)

register = Library()

@register.inclusion_tag('google_analytics/code.html')
def google_analytics_code(analytics_id=GOOGLE_ANALYTICS_ID):
    return {'google_analytics_id': analytics_id}
