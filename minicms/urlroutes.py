from .models import Page
from django import http
from django.views.generic.simple import direct_to_template
from urlrouter.base import URLHandler

class PageRoutes(URLHandler):
    model = Page

    def show(self, request, page):
        # TODO: Use permission check instead of is_admin. But first
        # think the whole permission management through...
        if not page.published and not request.user.is_admin:
            raise http.Http404('Not found')
        return direct_to_template(request, 'minicms/page_detail.html',
            {'page': page})
