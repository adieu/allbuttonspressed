from .models import Page
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template

def show(request, url):
    page = get_object_or_404(Page, url=url)
    return direct_to_template(request, 'minicms/page_detail.html',
        {'page': page})
