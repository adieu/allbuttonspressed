from djangoappengine.settings_base import *

SITE_NAME = 'All buttons pressed'
SITE_DESCRIPTION = 'Hacking the cloud with Django and SproutCore. Mostly on App Engine.'
SITE_COPYRIGHT = 'Waldemar Kornewald & Thomas Wanschik'
DISQUS_SHORTNAME = 'allbuttonspressed'

SECRET_KEY = '=r-$b*8hglm+858&9t043hlm6-&6-3d3vfc4((7yd0dbrakhvi'

INSTALLED_APPS = (
    'djangoappengine',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'minicms',
    'blog',
    'disqus',
)

MIDDLEWARE_CLASSES = (
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

import os
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)
