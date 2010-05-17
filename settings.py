# Django settings for sylph project.

import os

ROOT_URLCONF = 'sylph.urls'

TEMPLATE_DIRS = (os.path.join(os.path.abspath('.'), 'templates'),)

MEDIA_ROOT = os.path.join(os.path.abspath('.'), 'public')
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = False

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.load_template_source',
	'django.template.loaders.app_directories.load_template_source',
	#'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

INSTALLED_APPS = (
    #'django.contrib.auth',
    #'django.contrib.contenttypes',
    #'django.contrib.sessions',
    #'django.contrib.sites',

	'sylph.core.endpoint',
	#'sylph.system.backend',
	#'sylph.system.frontend',

	'sylph.apps.posts',
	'sylph.apps.images',
	#'sylph.apps.social',
)

try:
    from settings_local import *
except ImportError:
    pass

