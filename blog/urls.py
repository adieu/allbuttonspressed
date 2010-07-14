from django.conf.urls.defaults import *

urlpatterns = patterns('blog.views',
    (r'^(?P<blog_url>[^/]+)/feed/latest$', 'latest_entries_feed'),
    (r'^(?P<blog_url>[^/]+)/review/(?P<review_key>.*)$', 'review'),
    (r'^(?P<blog_url>[^/]+)/(?P<year>\d\d\d\d)/(?P<month>\d\d)/(?P<post_url>.+)$', 'show'),
    (r'^(?P<blog_url>[^/]+)$', 'browse'),
)
