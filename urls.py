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
    from mediagenerator.urls import urlpatterns as mediaurls
    urlpatterns += mediaurls
elif settings.DEBUG:
    path = os.path.join(os.path.dirname(__file__), '_generated_media')
    urlpatterns += patterns('',
        (r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL),
            'django.views.static.serve',
            {'document_root': path}),
    )
