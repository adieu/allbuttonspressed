from ..models import Blog
from django.template import Library

register = Library()

@register.inclusion_tag('blog/feeds.html')
def blog_feeds():
    blogs = Blog.objects.all()
    return {'blogs': blogs}

@register.inclusion_tag('blog/feeds.html')
def blog_feed(blog):
    return {'blogs': (blog,)}
