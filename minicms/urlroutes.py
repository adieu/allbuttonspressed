from .models import Page
from django.views.generic.simple import direct_to_template
from urlrouter.base import URLHandler

class PageRoutes(URLHandler):
    model = Page

    def show(self, request, page):
        return direct_to_template(request, 'minicms/page_detail.html',
            {'page': page})
