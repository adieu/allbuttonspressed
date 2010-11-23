from django.conf import settings

def cms(request):
    base_url = 'http%s://%s' % ('s' if request.is_secure() else '',
                                request.get_host())

    return {
        'site_name': settings.SITE_NAME,
        'site_copyright': settings.SITE_COPYRIGHT,
        'google_analytics_id': getattr(settings, 'GOOGLE_ANALYTICS_ID', None),
        'google_custom_search_id': getattr(settings, 'GOOGLE_CUSTOM_SEARCH_ID',
                                           None),
    }
