from .models import Blog, Post
from django.conf import settings
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list
from django.views.generic.simple import direct_to_template

FEEDBURNER_URL = 'http://feeds.feedburner.com/%s'
POSTS_PER_PAGE = 5

def show(request, blog_url, post_url):
    post = get_object_or_404(Post, url=post_url, blog=blog_url)
    return direct_to_template(request, 'blog/post_detail.html',
        {'post': post})

def browse(request, blog_url):
    blog = get_object_or_404(Blog, base_url=blog_url)
    query = Post.objects.filter(blog=blog, published=True)
    query = query.order_by('-published_on')
    return object_list(request, query, paginate_by=POSTS_PER_PAGE,
        extra_context={'blog': blog})

def feedburner(feed):
    """Converts a feed into a FeedBurner-aware feed."""
    def _feed(request, blog_url):
        blog = get_object_or_404(Blog, base_url=blog_url)
        if not blog.feedburner_name or \
                request.META['HTTP_USER_AGENT'].startswith('FeedBurner'):
            return feed(request, blog=blog)
        return HttpResponseRedirect(FEEDBURNER_URL % blog.feedburner_name)
    return _feed

class LatestEntriesFeed(Feed):
    def get_object(self, request, blog):
        return blog

    def title(self, blog):
        return '%s - %s' % (blog.title, settings.SITE_NAME)

    def link(self, blog):
        return blog.get_feed_url()

    def description(self, blog):
        return blog.description

    def item_title(self, post):
        return post.title

    def item_description(self, post):
        return post.rendered_content

    def items(self, blog):
        return Post.objects.filter(blog=blog).order_by('-published_on')[:50]

latest_entries_feed = feedburner(LatestEntriesFeed())
