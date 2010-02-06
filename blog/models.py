from .utils import slugify
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink

class Blog(models.Model):
    base_url = models.CharField('Base URL', primary_key=True, max_length=200,
        help_text='Example: With base URL "personal" your blog posts would be '
                  'below /blog/personal/...<br />'
                  'Slashes ("/") are not allowed in this field.')
    title = models.CharField(max_length=200,
        help_text='This will also be your feed title')
    description = models.CharField(max_length=500, blank=True,
        help_text='This will also be your feed description')
    feedburner_name = models.CharField('FeedBurner name', max_length=200, blank=True,
        help_text='Optional (specify this if you want this blog to publish '
                  'its feeds via FeedBurner)')

    def __unicode__(self):
        return self.title

    @permalink
    def get_feed_url(self):
        return ('blog.views.latest_entries_feed', (),
                {'blog_url': self.base_url})

def default_blog():
    try:
        return Blog.objects.get()
    except Blog.DoesNotExist:
        return None

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    blog = models.ForeignKey(Blog, related_name='posts',
        default=default_blog)
    published = models.BooleanField(default=False)
    author = models.ForeignKey(User, related_name='posts', null=True, blank=True,
        help_text='Optional (filled automatically when saving)')
    url = models.CharField('URL', blank=True, max_length=200,
        help_text='Optional (filled automatically when publishing)')
    published_on = models.DateTimeField(null=True, blank=True,
        help_text='Optional (filled automatically when publishing)')
    last_update = models.DateTimeField(auto_now=True)

    @property
    def rendered_content(self):
        from django.template.defaultfilters import linebreaks
        from django.utils.safestring import mark_safe
        return linebreaks(mark_safe(self.content))

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ('blog.views.show', (),
                {'post_url': self.url, 'blog_url': self.blog_id})

    def save(self, *args, **kwargs):
        if self.published and not self.published_on:
            self.published_on = datetime.now()
        if self.published and not self.url:
            self.url = '%s-%s' % (self.published_on.strftime('%Y-%m-%d'),
                                  slugify(self.title))
        super(Post, self).save(*args, **kwargs)
