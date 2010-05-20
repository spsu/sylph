# Django settings for sylph project.

import os

ROOT_URLCONF = 'sylph.urls'

TEMPLATE_DIRS = (os.path.join(os.path.abspath('.'), 'templates'),)

MEDIA_ROOT = os.path.join(os.path.abspath('.'), 'public')
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'
LOGIN_URL = '/system/login/'
LOGIN_REDIRECT_URL = '/'

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = False

TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.load_template_source', 
	'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.core.context_processors.auth',
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
	#'django.contrib.messages.context_processors.messages',
)



MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
	'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.sites',

	'sylph.core.endpoint',
	#'sylph.system.backend',
	#'sylph.system.frontend',

	'sylph.apps.posts',
	#'sylph.apps.social',
)

try:
    from settings_local import *
except ImportError:
    pass

