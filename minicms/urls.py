from django.conf.urls.defaults import *

urlpatterns = patterns('minicms.views',
    (r'^(?P<url>.*)$', 'show'),
)
