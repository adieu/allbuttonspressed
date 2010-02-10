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
                  '# numbered list<br /><br />'
                  '.. sourcecode:: python<br /><br />'
                  '&nbsp;&nbsp;&nbsp;def f(x):<br />'
                  '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;pass</code>'
                  '<br /><br />'
                  'See the <a href="'
                  'http://docutils.sourceforge.net/docs/user/rst/quickref.html'
                  '" target="_blank">quick reference</a> for more details.')
    # This stores the generated HTML code from our wiki syntax
    pre_rendered_content = models.TextField(blank=True, editable=False)

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
