from django.conf.urls.defaults import *
from django.conf import settings
from blog.models import PostsSitemap
import os
import re

handler500 = 'djangotoolbox.errorviews.server_error'

sitemaps = {
    'tag': PostsSitemap,
}

urlpatterns = patterns('',
    (r'^admin/', include('urlsadmin')),
    (r'^blog/', include('blog.urls')),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)

if settings.MEDIA_DEV_MODE:
    # Generate media on-the-fly
    from mediagenerator.urls import urlpatterns as mediaurls
    urlpatterns += mediaurls
