from django.db import models

class BaseContent(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True,
        help_text='Please use reStructuredText, here. See the <a href="http://docutils.sourceforge.net/docs/user/rst/quickref.html" target="_blank">quick reference</a> for more details.')
    pre_rendered_content = models.TextField(blank=True, editable=False)

    @property
    def rendered_content(self):
        from django.utils.safestring import mark_safe
        return mark_safe(self.pre_rendered_content)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        from .markup import html_body
        self.pre_rendered_content = html_body(self.content)
        super(BaseContent, self).save(*args, **kwargs)

class Page(BaseContent):
    url = models.CharField('URL', primary_key=True, max_length=200)

    def __unicode__(self):
        return u"%s -- %s" % (self.url, self.title)

    def get_absolute_url(self):
        return self.url

class Config(models.Model):
    name = models.CharField(primary_key=True, max_length=200)
    content = models.TextField(blank=True)

    def __unicode__(self):
        return self.name
