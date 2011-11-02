from django.conf import settings
from django.conf.urls.defaults import *
from blog.models import PostsSitemap
from minicms.models import PagesSitemap

handler500 = 'djangotoolbox.errorviews.server_error'

sitemaps = {
    'posts': PostsSitemap,
    'pages': PagesSitemap,
}

urlpatterns = patterns('',
    (r'^admin/', include('urlsadmin')),
    (r'^blog/', include('blog.urls')),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}),
    (r'^search$', 'google_cse.views.search'),
    (r'^robots\.txt$', 'robots.views.robots'),
)

if 'djangoappengine' in settings.INSTALLED_APPS:
    urlpatterns = patterns('',
        ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    ) + urlpatterns
