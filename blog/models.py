from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
import re

_NORMALIZE = re.compile(r'\W+', re.UNICODE)

def slugify(text):
    return _NORMALIZE.sub('-', text).strip('-')

class Blog(models.Model):
    base_url = models.CharField('Base URL', primary_key=True, max_length=200)
    title = models.CharField(max_length=200)#

    def __unicode__(self):
        return self.title

class Post(models.Model):
    url = models.CharField('URL', primary_key=True, blank=True, max_length=200,
        help_text='Optional (filled automatically)')
    author = models.ForeignKey(User, related_name='posts', null=True, blank=True,
        help_text='Optional (filled automatically)')
    blog = models.ForeignKey(Blog, related_name='posts',
        default=lambda: Blog.objects.all()[0])
    title = models.CharField(max_length=200)
    content = models.TextField()
    published = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.url

    def save(self, *args, **kwargs):
        if not self.url:
            self.url = '%s/%s-%s' % (self.blog.base_url,
                                     datetime.now().strftime('%Y-%M-%d'),
                                     slugify(self.title))
        super(Post, self).save(*args, **kwargs)
