from django.conf import settings

def cms(request):
    return {
        'site_name': settings.SITE_NAME,
        'site_copyright': settings.SITE_COPYRIGHT,
    }
