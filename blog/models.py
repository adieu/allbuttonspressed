from .utils import slugify
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.sitemaps import Sitemap
from django.db import models
from django.db.models import permalink
from minicms.models import BaseContent
import re

FEEDBURNER_ID = re.compile(r'^http://feeds.feedburner.com/([^/]+)/?$')

class Blog(models.Model):
    base_url = models.CharField('Base URL', max_length=200,
        help_text='Example: With base URL "personal" your blog posts would '
                  'be below /blog/personal/...<br />'
                  'Slashes ("/") are not allowed in this field.<br />')
    title = models.CharField(max_length=200,
        help_text='This will also be your feed title')
    description = models.CharField(max_length=500, blank=True,
        help_text='This will also be your feed description')
    feed_redirect_url = models.URLField('Feed redirect URL',
        verify_exists=False, blank=True,
        help_text='Optional (use this to publish feeds via FeedBurner)<br />'
                  'Example: http://feeds.feedburner.com/YourFeedBurnerID<br />'
                  'If you use FeedBurner this will also enable FeedFlares.')

    def __unicode__(self):
        return self.title

    def feedburner_id(self):
        # Detect FeedBurner ID from feed redirect URL
        match = FEEDBURNER_ID.match(self.feed_redirect_url)
        if match:
            return match.group(1)
        return None

    @permalink
    def get_feed_url(self):
        return ('blog.views.latest_entries_feed', (),
                {'blog_url': self.base_url})

def default_blog():
    blogs = Blog.objects.all()[:1]
    if blogs:
        return blogs[0]
    return None

class Post(BaseContent):
    blog = models.ForeignKey(Blog, related_name='posts',
        default=default_blog,
        help_text="Changing the blog will also change the post's URL, so "
                  "better don't change it for a published post.")
    published = models.BooleanField(default=False)
    author = models.ForeignKey(User, related_name='posts', null=True, blank=True,
        help_text='Optional (filled automatically when saving)')
    url = models.CharField('URL', blank=True, max_length=200,
        help_text='Optional (filled automatically when publishing)')
    published_on = models.DateTimeField(null=True, blank=True,
        help_text='Optional (filled automatically when publishing)')
    last_update = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ('blog.views.show', (),
                {'post_url': self.url, 'blog_url': self.blog.base_url,
                 'year': self.published_on.year,
                 'month': '%02d' % self.published_on.month})

    def save(self, *args, **kwargs):
        if self.published and not self.published_on:
            self.published_on = datetime.now()
        if self.published and not self.url:
            self.url = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

class PostsSitemap(Sitemap):
    changefreq = "daily"

    def items(self):
        return Post.objects.filter(published=True).order_by('-published_on')[:2000]

    def lastmod(self, obj):
        return obj.last_update
