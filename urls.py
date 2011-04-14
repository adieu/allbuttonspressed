from django.conf.urls.defaults import *
from blog.models import PostsSitemap
from minicms.models import PagesSitemap

handler500 = 'djangotoolbox.errorviews.server_error'

sitemaps = {
    'posts': PostsSitemap,
    'pages': PagesSitemap,
}

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    (r'^admin/', include('urlsadmin')),
    (r'^blog/', include('blog.urls')),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}),
    (r'^search$', 'django.views.generic.simple.direct_to_template',
        {'template': 'search.html'}),
    (r'^robots\.txt$', 'robots.views.robots'),
)
