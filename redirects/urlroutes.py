from .models import Redirect
from django import http
from urlrouter.base import URLHandler

class RedirectRoutes(URLHandler):
    model = Redirect

    def show(self, request, redirect):
        if not redirect.redirect_to:
            return http.HttpResponseGone()
        return http.HttpResponsePermanentRedirect(redirect.redirect_to)
