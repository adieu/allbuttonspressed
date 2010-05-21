try:
    from djangoappengine.settings_base import *
    has_djangoappengine = True
except ImportError:
    has_djangoappengine = False
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

import os

# Uncomment the following if you want to use MongoDB
# -----------------
#DATABASES = {
#    'default': {
#        'ENGINE': 'django_mongodb_engine.mongodb',
#        'NAME': 'test',
#        'USER': '',
#        'PASSWORD': '',
#        'HOST': 'localhost',
#        'PORT': '27017',
#        'SUPPORTS_TRANSACTIONS': False,
#    }
#}
# -----------------

SITE_NAME = 'All buttons pressed'
SITE_DESCRIPTION = 'Hacking the cloud with Django on non-relational DBs.'
SITE_COPYRIGHT = 'the author'
DISQUS_SHORTNAME = 'allbuttonspressed'
GOOGLE_ANALYTICS_ID = 'UA-12334792-3'
# Get the ID from the CSE "Basics" control panel ("Search engine unique ID")
GOOGLE_CUSTOM_SEARCH_ID = '013842355536421310315:sg4lqatbb1y'
# Set RT username for retweet buttons
TWITTER_USERNAME = 'wkornewald'
# In order to always have uniform URLs in retweets and FeedBurner we redirect
# any access to URLs that are not in ALLOWED_DOMAINS to the first allowed
# domain. You can have additional domains for testing.
ALLOWED_DOMAINS = ('www.allbuttonspressed.com',)

SECRET_KEY = '=r-$b*8hglm+858&9t043hlm6-&6-3d3vfc4((7yd0dbrakhvi'

SITE_ID = 4094

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'minicms',
    'blog',
    'disqus',
)

if has_djangoappengine:
    INSTALLED_APPS = ('djangoappengine',) + INSTALLED_APPS

MIDDLEWARE_CLASSES = (
    'djangotoolbox.middleware.RedirectMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'minicms.middleware.CMSFallbackMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'minicms.context_processors.cms',
)

USE_I18N = False

ADMIN_MEDIA_PREFIX = '/media/admin/'
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)

ROOT_URLCONF = 'urls'
