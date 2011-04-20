from .models import Blog, Post
from .views import browse, show_post, latest_entries_feed
from urlrouter.base import URLHandler

class BlogRoutes(URLHandler):
    model = Blog

    def show(self, request, blog):
        if request.path == blog.get_internal_feed_url():
            return latest_entries_feed(request, blog)
        return browse(request, blog=blog)

    def get_urls(self, blog):
        yield blog.get_absolute_url()
        yield blog.get_internal_feed_url()

class BlogPostRoutes(URLHandler):
    model = Post
    show = staticmethod(show_post)

    def get_urls(self, post):
        if post.published:
            yield post.get_absolute_url()
