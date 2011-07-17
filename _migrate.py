# Run the migration function via manage.py remote shell (or manage.py shell
# for local development DB)

from datetime import datetime
from blog.models import Blog, Post
from minicms.models import Page
from django.db import models
from redirects.models import Redirect

def migrate_v2():
    # Run this *before* deployment
    Page._meta.get_field('last_update').default = lambda: datetime.now()
    for page in Page.objects.all():
        page.save()

def migrate_v3():
    # Run this quickly before or after deployment
    Blog.add_to_class('base_url', models.CharField('Base URL', max_length=200))
    for blog in Blog.objects.all():
        blog.url = '/blog/' + blog.base_url
        blog.save()

    Post._meta.get_field('last_update').auto_now = False
    for post in Post.objects.all():
        if post.url and post.published_on and '/' not in post.url:
            post.url = post.blog.url_prefix + '%04d/%02d/' % (post.published_on.year, post.published_on.month) + post.url
        post.save()

    Page._meta.get_field('last_update').auto_now = False
    for page in Page.objects.all():
        page.save()

def migrate_v4():
    # Added "published" field
    Page._meta.get_field('last_update').auto_now = False
    for page in Page.objects.all():
        page.published = True
        page.save()

def migrate_v5():
    # Updated docutils and Pygments and switched to HTML writer that uses
    # <code> instead of <tt> tags (the latter are invalid in HTML5)
    resave_content()

def resave_content():
    for post in Post.objects.all():
        post.save()
    for page in Page.objects.all():
        page.save()

class DjangoRedirect(models.Model):
    __module__ = 'redirects.models'

    old_path = models.CharField(max_length=200)
    new_path = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'django_redirect'

    def __unicode__(self):
        return "%s ---> %s" % (self.old_path, self.new_path)

def migrate_redirects():
    for redirect in DjangoRedirect.objects.all():
        Redirect(redirect_from=redirect.old_path, redirect_to=redirect.new_path).save()
