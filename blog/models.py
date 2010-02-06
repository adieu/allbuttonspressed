from .utils import slugify
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models

class Blog(models.Model):
    base_url = models.CharField('Base URL', primary_key=True, max_length=200,
        help_text='Example: With base URL "personal" your blog posts would be '
                  'below /blog/personal/...<br />'
                  'Slashes ("/") are not allowed in this field.')
    title = models.CharField(max_length=200)#

    def __unicode__(self):
        return self.title

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

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.url

    def save(self, *args, **kwargs):
        if self.published and not self.published_on:
            self.published_on = datetime.now()
        if self.published and not self.url:
            self.url = '%s/%s-%s' % (self.blog.base_url,
                                     self.published_on.strftime('%Y-%m-%d'),
                                     slugify(self.title))
        super(Post, self).save(*args, **kwargs)
