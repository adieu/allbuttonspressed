from .models import Blog, Post
from datetime import datetime
from django.conf import settings
from django.contrib.syndication.views import Feed
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.utils.feedgenerator import Atom1Feed
from django.views.generic import ListView
from simplesocial.api import wide_buttons, narrow_buttons

def review(request, review_key):
    post = get_object_or_404(Post, review_key=review_key)
    return show_post(request, post, review=True)

def show_post(request, post, review=False):
    recent_posts = Post.objects.filter(blog=post.blog, published=True)
    recent_posts = recent_posts.order_by('-published_on')[:6]
    return render(request, 'blog/post_detail.html',
        {'post': post, 'blog': post.blog, 'recent_posts': recent_posts,
         'review': review})

class BrowseView(ListView):
    paginate_by = 8

    def dispatch(self, request, blog):
        if request.GET.get('page') == '1':
            return HttpResponseRedirect(request.path)
        return super(BrowseView, self).dispatch(request, blog=blog)

    def get_queryset(self):
        query = Post.objects.filter(blog=self.kwargs['blog'], published=True)
        # TODO: add select_related('author')
        return query.order_by('-published_on')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BrowseView, self).get_context_data(**kwargs)
        context.update({'blog': self.kwargs['blog'],
                        'recent_posts': self.get_queryset()[:6],
                        'browse_posts': True})
        return context

browse = BrowseView.as_view()

def feedburner(feed):
    """Converts a feed into a FeedBurner-aware feed."""
    def _feed(request, blog):
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
        return blog.title

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
        header = wide_buttons(self._request, post.title, post.get_absolute_url())
        footer = narrow_buttons(self._request, post.title, post.get_absolute_url())
        footer += '<p><a href="%s#disqus_thread">Leave a comment</a></p>' % url
        return header + post.rendered_content + footer

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
