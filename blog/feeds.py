from django.http import HttpResponseRedirect
from django.conf import settings

class FeedburnerMiddleware(object):
    '''
    Redirect the user to a feedburner feed for basic feeds
    '''
    def __init__(self):
        self.base_url = '%s%%s' % getattr(settings, 'FEEDBURNER_URL', 'http://feeds.feedburner.com/')

    def process_request(self, request):
        try:
            func, args, kwargs = resolve(request.path)
        except Resolver404:
            return None
        feeds = settings.FEEDBURNER.get(Site.objects.get_current().domain, {})
        if (not feeds or                                         # disabled
            func.__name__ not in ('redirect_to_feed', 'feed') or # not a feed
            kwargs['url'] not in feeds):                         # not served in feedburner
            return None

        if request.META['HTTP_USER_AGENT'].startswith('FeedBurner'):
            return None # feedburner must get feed as is
        else:
            return HttpResponseRedirect(self.base_url % feeds[kwargs['url']])
