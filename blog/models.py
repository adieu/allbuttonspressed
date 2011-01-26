from .utils import slugify
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.sitemaps import Sitemap
from django.db import models
from django.db.models import permalink
from minicms.models import BaseContent
from random import choice
from string import ascii_letters, digits
import re

FEEDBURNER_ID = re.compile(r'^http://feeds\d*.feedburner.com/([^/]+)/?$')

class Blog(models.Model):
    title = models.CharField(max_length=200,
        help_text='This will also be your feed title')
    keywords = models.CharField(max_length=200, blank=True,
        help_text='Optional: Add a short extra description for the title tag '
                  '(for SEO-purposes).')
    url = models.CharField('URL', max_length=200,
        help_text='Example: /blog')
    description = models.CharField(max_length=500, blank=True,
        help_text='This will also be your feed description.')
    feed_redirect_url = models.URLField('Feed redirect URL',
        verify_exists=False, blank=True,
        help_text='Optional (use this to publish feeds via FeedBurner)<br />'
                  'Example: http://feeds.feedburner.com/YourFeedBurnerID<br />'
                  'If you use FeedBurner this will also enable FeedFlares.')

    def __unicode__(self):
        return self.title

    @property
    def url_prefix(self):
        if self.url.endswith('/'):
            return self.url
        return self.url + '/'

    def feedburner_id(self):
        # Detect FeedBurner ID from feed redirect URL
        match = FEEDBURNER_ID.match(self.feed_redirect_url)
        if match:
            return match.group(1)
        return None

    def get_absolute_url(self):
        return self.url

    def get_feed_url(self):
        return self.feed_redirect_url or self.get_internal_feed_url()

    def get_internal_feed_url(self):
        return self.url_prefix + 'feed/latest'

def default_blog():
    blogs = Blog.objects.all()[:1]
    if blogs:
        return blogs[0]
    return None

def generate_review_key():
    charset = ascii_letters + digits
    return ''.join(choice(charset) for i in range(32))

class Post(BaseContent):
    blog = models.ForeignKey(Blog, related_name='posts', default=default_blog)
    published = models.BooleanField(default=False)
    author = models.ForeignKey(User, related_name='posts', null=True, blank=True,
        help_text='Optional (filled automatically when saving)')
    url = models.CharField('URL', blank=True, max_length=200,
        help_text='Optional (filled automatically when publishing). Better '
                  'use a hand-optimized URL that is unique and SEO-friendly.<br/>'
                  'Tip: Relative URLs (not starting with "/") will be prefixed '
                  "with the blog's URL.")
    published_on = models.DateTimeField(null=True, blank=True,
        help_text='Optional (filled automatically when publishing)')
    review_key = models.CharField(max_length=32, blank=True,
        help_text='Optional (filled automatically when saving)')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        if not self.published:
            return self.get_review_url()
        return self.url

    @permalink
    def get_review_url(self):
        return ('blog.views.review', (), {'review_key': self.review_key})

    def save(self, *args, **kwargs):
        if not self.review_key:
            self.review_key = generate_review_key()
        if self.published and not self.published_on:
            self.published_on = datetime.now()
        if self.published and not self.url:
            self.url = self.blog.url_prefix + slugify(self.title)
        elif self.published and not self.url.startswith('/'):
            self.url = self.blog.url_prefix + self.url
        super(Post, self).save(*args, **kwargs)

class PostsSitemap(Sitemap):
    changefreq = "daily"

    def items(self):
        return Post.objects.filter(published=True).order_by('-published_on')[:2000]

    def lastmod(self, obj):
        return obj.last_update

from . import posts_page_dependency
