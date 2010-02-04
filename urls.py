from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^admin/', include('urlsadmin')),
    (r'^(?P<url>.*)$', 'minicms.views.show'),
)
