from django.conf import settings

def cms(request):
    return {
        'site_name': settings.SITE_NAME,
        'site_description': settings.SITE_DESCRIPTION,
    }
