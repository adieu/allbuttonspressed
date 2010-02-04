from .models import Page
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from django.utils.safestring import mark_safe

DEFAULT_TEMPLATE = 'minicms/default.html'

def show(request, url):
    page = get_object_or_404(Page, url='/'+url)

    # To avoid having to always use the "|safe" filter in flatpage templates,
    # mark the title and content as already safe (since they are raw HTML
    # content in the first place).
    page.title = mark_safe(page.title)
    page.content = mark_safe(page.content)

    return direct_to_template(request, DEFAULT_TEMPLATE,
        extra_context={'page': page})
