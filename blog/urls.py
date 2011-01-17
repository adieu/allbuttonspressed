from django.conf.urls.defaults import *

urlpatterns = patterns('blog.views',
    (r'^review/(?P<review_key>.*)$', 'review'),
)
