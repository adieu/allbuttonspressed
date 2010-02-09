from .views import show
from django.http import Http404, HttpResponseRedirect
from django.conf import settings

class RedirectMiddleware(object):
    def process_request(self, request):
        host = request.get_host().split(':')[0]
        if settings.DEBUG or host == 'testserver' or \
                not getattr(settings, 'ALLOWED_DOMAINS', None):
            return
        if host not in settings.ALLOWED_DOMAINS:
            return HttpResponseRedirect('http://' + settings.ALLOWED_DOMAINS[0])

class CMSFallbackMiddleware(object):
    def process_response(self, request, response):
        if response.status_code != 404:
            return response # No need to check for a flatpage for non-404 responses.
        try:
            return show(request, request.path_info)
        # Return the original response if any errors happened. Because this
        # is a middleware, we can't assume the errors will be caught elsewhere.
        except Http404:
            return response
        except:
            if settings.DEBUG:
                raise
            return response
