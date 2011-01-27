from django.contrib.sitemaps import Sitemap
from django.db import models

class BaseContent(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True,
        help_text='Syntax examples (reStructuredText):<br /><br />'
                  '<code><span style="font-weight: bold">**bold**</span>'
                  '&nbsp;&nbsp;<em>*italicts*</em>&nbsp;&nbsp;'
                  '``inline_code()``&nbsp;&nbsp;'
                  '`long link &lt;http://url.com&gt;`_ and `short link`_<br />'
                  '.. _short link: http://url.com'
                  '  <em>(put this at the bottom)</em>'
                  '<br /><br />'
                  '* bulleted list<br />'
                  '#. numbered list<br /><br />'
                  '.. image:: http://example.com/image.png<br /><br />'
                  '.. sourcecode:: python<br /><br />'
                  '&nbsp;&nbsp;&nbsp;def f(x):<br />'
                  '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;pass</code>'
                  '<br /><br />'
                  'See the <a href="'
                  'http://docutils.sourceforge.net/docs/user/rst/quickref.html'
                  '" target="_blank">quick reference</a> for more details.')
    # This stores the generated HTML code from our wiki syntax
    pre_rendered_content = models.TextField(blank=True, editable=False)
    last_update = models.DateTimeField(auto_now=True)

    @property
    def rendered_content(self):
        from django.utils.safestring import mark_safe
        return mark_safe(self.pre_rendered_content)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Pre-generate HTML code from our markup for faster access, later
        from .markup import html_body
        self.pre_rendered_content = html_body(self.content)
        super(BaseContent, self).save(*args, **kwargs)

class Page(BaseContent):
    url = models.CharField('URL', max_length=200)
    show_share_buttons = models.BooleanField(default=True,
        help_text='Show buttons for sharing this page on Twitter, Facebook, etc.')
    published = models.BooleanField(default=True)

    def __unicode__(self):
        return u"%s -- %s" % (self.url, self.title)

    def get_absolute_url(self):
        return self.url

class Block(models.Model):
    name = models.CharField(max_length=200)
    content = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class PagesSitemap(Sitemap):
    changefreq = "daily"

    def items(self):
        return Page.objects.filter(published=True)[:2000]

    def lastmod(self, obj):
        return obj.last_update
