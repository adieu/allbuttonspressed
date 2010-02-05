from .models import Post
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from django.utils.safestring import mark_safe

DEFAULT_TEMPLATE = 'blog/default.html'

def show(request, url):
    post = get_object_or_404(Post, url=url, published=True)

    # To avoid having to always use the "|safe" filter in flatpage templates,
    # mark the title and content as already safe (since they are raw HTML
    # content in the first place).
    post.title = mark_safe(post.title)
    post.content = mark_safe(post.content)

    return direct_to_template(request, DEFAULT_TEMPLATE,
        extra_context={'post': post})

def browse(request, blog_url):

