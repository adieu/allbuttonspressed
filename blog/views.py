from .models import Blog, Post
from datetime import datetime
from django.conf import settings
from django.contrib.syndication.views import Feed
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.utils.feedgenerator import Atom1Feed
from django.views.generic.list_detail import object_list
from django.views.generic.simple import direct_to_template

POSTS_PER_PAGE = 8
TWEETMEME_FEED_BUTTON = '<a href="http://api.tweetmeme.com/share?url=%(url)s" style="float: left; margin-right: 10px;"><img src="http://api.tweetmeme.com/imagebutton.gif?url=%(url)s" height="61" width="51" /></a>'

def review(request, blog_url, review_key):
    blog = get_object_or_404(Blog, base_url=blog_url)
    post = get_object_or_404(Post, review_key=review_key)
    return show_post(request, blog, post, review=True)

def show(request, blog_url, year, month, post_url):
    try:
        start = datetime(int(year), int(month), 1)
        if month == 12:
            end = datetime(int(year)+1, 1, 1)
        else:
            end = datetime(int(year), int(month)+1, 1)
    except ValueError:
        raise Http404('Date format incorrect')
    blog = get_object_or_404(Blog, base_url=blog_url)
    post = get_object_or_404(Post, url=post_url, blog=blog, published=True,
        published_on__gte=start, published_on__lt=end)
    return show_post(request, blog, post, review=False)

def show_post(request, blog, post, review=False):
    recent_posts = Post.objects.filter(blog=blog, published=True)
    recent_posts = recent_posts.order_by('-published_on')[:6]

    return direct_to_template(request, 'blog/post_detail.html',
        {'post': post, 'blog': blog, 'recent_posts': recent_posts,
         'review': review})

def browse(request, blog_url):
    blog = get_object_or_404(Blog, base_url=blog_url)
    query = Post.objects.filter(blog=blog, published=True)
    query = query.order_by('-published_on')
    # TODO: add select_related('author')
    return object_list(request, query, paginate_by=POSTS_PER_PAGE,
        extra_context={'blog': blog, 'recent_posts': query[:6],
                       'browse_posts': True})

def feedburner(feed):
    """Converts a feed into a FeedBurner-aware feed."""
    def _feed(request, blog_url):
        blog = get_object_or_404(Blog, base_url=blog_url)
        if not blog.feed_redirect_url or \
                request.META['HTTP_USER_AGENT'].startswith('FeedBurner') or \
                request.GET.get('override-redirect') == '1':
            return feed(request, blog=blog)
        return HttpResponseRedirect(blog.feed_redirect_url)
    return _feed

class LatestEntriesFeed(Feed):
    feed_type = Atom1Feed

    def get_object(self, request, blog):
        return blog

    def title(self, blog):
        return '%s - %s' % (blog.title, settings.SITE_NAME)

    def link(self, blog):
        return blog.get_absolute_url()

    def subtitle(self, blog):
        return blog.description

    def item_title(self, post):
        return post.title

    def item_description(self, post):
        url = 'http%s://%s%s' % ('s' if self._request.is_secure() else '',
                                 self._request.get_host(),
                                 post.get_absolute_url())
        header = TWEETMEME_FEED_BUTTON % {'url': url}
        return header + post.rendered_content

    def item_author_name(self, post):
        return post.author.get_full_name()

    def item_pubdate(self, post):
        return post.published_on

    def items(self, blog):
        query = Post.objects.filter(blog=blog, published=True).order_by(
            '-published_on')
        # TODO: add select_related('author') once it's supported
        return query[:100]

@feedburner
def latest_entries_feed(request, *args, **kwargs):
    feed = LatestEntriesFeed()
    feed._request = request
    return feed(request, *args, **kwargs)
