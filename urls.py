from django.conf.urls.defaults import *
from blog.models import PostsSitemap

sitemaps = {
    'tag': PostsSitemap,
}

urlpatterns = patterns('',
    (r'^admin/', include('urlsadmin')),
    (r'^blog/', include('blog.urls')),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps})

)
