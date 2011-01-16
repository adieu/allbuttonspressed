from django.core.urlresolvers import reverse
from django.template import loader, RequestContext
from djangotoolbox.http import TextResponse

def robots(request):
    sitemap_url = reverse('django.contrib.sitemaps.views.sitemap')
    sitemap_url = 'http%s://%s%s' % ('s' if request.is_secure() else '',
                                     request.get_host(),
                                     sitemap_url)
    t = loader.get_template('robots/robots.txt')
    c = RequestContext(request, {
        'sitemap_url': sitemap_url,
    })
    return TextResponse(t.render(c))
