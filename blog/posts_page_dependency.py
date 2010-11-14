from .models import Post
from django.db import models
from django.db.models.signals import pre_save, post_save
try:
    from django.dispatch import receiver
except ImportError:
    def receiver(signal, **kwargs):
        def _decorator(func):
            signal.connect(func, **kwargs)
            return func
        return _decorator
from minicms.models import Page

# Handle dependency on blog posts by updating the respective page
# whenever a blog post gets changed
Page.add_to_class('depends_on_blog_posts',
                  models.BooleanField(default=False, editable=False))

@receiver(pre_save, sender=Page)
def update_dependency_field(sender, instance, **kwargs):
    instance.depends_on_blog_posts = '.. blogposts::' in instance.content

@receiver(post_save, sender=Post)
def update_blog_dependencies(sender, **kwargs):
    for page in Page.objects.filter(depends_on_blog_posts=True):
        page.save()
