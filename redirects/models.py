from django.db import models

class Redirect(models.Model):
    redirect_from = models.CharField(max_length=200, unique=True,
        help_text='Example: /about')
    redirect_to = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return "%s ---> %s" % (self.redirect_from, self.redirect_to)

    def get_absolute_url(self):
        return self.redirect_from
