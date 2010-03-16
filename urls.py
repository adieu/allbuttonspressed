from django.conf.urls.defaults import *
from blog.models import PostsSitemap

handler500 = 'djangotoolbox.errorviews.server_error'

sitemaps = {
    'tag': PostsSitemap,
}

urlpatterns = patterns('',
    (r'^admin/', include('urlsadmin')),
    (r'^blog/', include('blog.urls')),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps})

)
