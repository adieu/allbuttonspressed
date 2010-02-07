from django.db import models

class Page(models.Model):
    url = models.CharField('URL', primary_key=True, max_length=200)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)

    @property
    def rendered_content(self):
        # XXX: We use linebreaksbr instead of linebreaks because the latter
        # breaks <pre> tags with incorrectly placed </p> closing tags.
        from django.template.defaultfilters import linebreaksbr
        from django.utils.safestring import mark_safe
        return linebreaksbr(mark_safe(self.content.strip()))

    def __unicode__(self):
        return u"%s -- %s" % (self.url, self.title)

    def get_absolute_url(self):
        return self.url

class Config(models.Model):
    name = models.CharField(primary_key=True, max_length=200)
    content = models.TextField(blank=True)

    def __unicode__(self):
        return self.name
