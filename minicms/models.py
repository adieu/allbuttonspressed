from django.db import models

class Page(models.Model):
    url = models.CharField('URL', primary_key=True, max_length=200)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)

    def __unicode__(self):
        return u"%s -- %s" % (self.url, self.title)

    def get_absolute_url(self):
        return self.url
