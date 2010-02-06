from django.conf.urls.defaults import *

urlpatterns = patterns('blog.views',
    (r'^(?P<blog_url>[^/]+)/feed/latest$', 'latest_entries_feed'),
    (r'^(?P<blog_url>[^/]+)/(?P<post_url>.+)$', 'show'),
    (r'^(?P<blog_url>[^/]+)$', 'browse'),
)
