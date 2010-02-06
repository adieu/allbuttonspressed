from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^admin/', include('urlsadmin')),
    (r'^blog/', include('blog.urls')),
    (r'', include('minicms.urls')),
)
