from . import api
from .views import show
from django.conf import settings
from django.http import Http404

class URLRouterFallbackMiddleware(object):
    def process_response(self, request, response):
        if response.status_code != 404:
            return response # Pass through non-404 responses
        try:
            # TODO/XXX: Workaround for bug in Django. TemplateResponse.render()
            # isn't called after process_response().
            new_response = show(request, request.path_info)
            if hasattr(new_response, 'render') and callable(new_response.render):
                new_response = new_response.render()
            return new_response
        # Return the original response if any errors happened. Because this
        # is a middleware, we can't assume the errors will be caught elsewhere.
        except Http404:
            return response
        except:
            if settings.DEBUG:
                raise
            return response
