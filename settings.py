# Django settings for sylph project.

import os
import sys

# ================= Version Information ===================
"""
	Both the software and Sylph protocol (which multiple softwares implement)
	utilize a similar versioning scheme:

		major.minor.bugfix.month.day (as MM and DD respectively)
"""

SOFTWARE_NAME = 'Sylph.py Client'
SOFTWARE_VERSION = '0.1.0.05.25'
PROTOCOL_VERSION = '0.1.0.05.25' 

# ================= Common Configuration ==================

ROOT_URLCONF = 'sylph.urls'

TEMPLATE_DIRS = (os.path.join(os.path.abspath('.'), 'templates'),)
MEDIA_ROOT = os.path.join(os.path.abspath('.'), 'public_static')

APPEND_SLASH = True
LOGIN_URL = '/system/login/'
LOGIN_REDIRECT_URL = '/'

MEDIA_URL = '' # XXX: Overridden in settings_local.py
ADMIN_MEDIA_PREFIX = '/media/'

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = False

INTERNAL_IPS = ('127.0.0.1')

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

	# Custom context processors
	'sylph.core.backend.utils.context_processors.settings',
	#'sylph.core.backend.utils.context_processors.ip_address',
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
	'django.contrib.humanize',

	'sylph.core.endpoint',
	'sylph.core.backend',
	#'sylph.core.frontend',

	'sylph.apps.posts',
	#'sylph.apps.social',
)

# ================= Virtualization Helpers ================
"""
	These functions make it easy to run multiple instances of Sylph to test the 
	communication abilities of the code. They allow binding of different URLs 
	and database schemas depending on which port the server is told to run on:

		python manage.py runserver [port]

	Port 8000 is considered the default.
"""

def get_port():
	"""Gets the port that python runserver was told to run on."""
	# FIXME: Very crude, only works if ONE argument is given!
	if len(sys.argv) < 3:
		return 8000
	return int(sys.argv[2])

def get_url(path = ""):
	"""Returns the URL with the port the server is running on, optionally with a
	path segment appended."""
	# FIXME: Not capable of binding different IP addresses!
	port = get_port()
	p = 'http://127.0.0.1%s/' % ("" if port == 80 else ":"+str(port))
	if path[0] == '/':
		p += path[1:]
	else:
		p += path

	if path[-1] != '/':
		p += '/'

	return p

def get_db(prefix = "sylph", port = None):
	"""Return the database name that the running instance will bind to. This
	varies based on the port django is told to run on."""
	if not port:
		port = get_port()
	if port == 8000:
		return prefix
	return prefix + str(port)


PORT = get_port() # XXX: Temporary for templates

# ================= Import Specific Configs ===============
		
try:
    from settings_local import *
except ImportError:
    pass

