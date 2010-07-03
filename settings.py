# Django settings for sylph project.

import os
import sys

# ================= Version Information ===================
"""
Both the software and Sylph protocol (which multiple softwares
may implement) utilize a similar versioning scheme:

major.minor.bugfix-year.month.day (as MM and DD respectively)
"""

SOFTWARE_NAME = 'Sylph.py Client'
SOFTWARE_VERSION = '0.1.0-10.05.25'
PROTOCOL_VERSION = '0.1.0-10.05.25'
RDF_SERIALIZATION = 'xml' # xml or n3

# ================= Environment ===========================

# Ensure local libraries can be loaded
sys.path.insert(0, os.path.abspath(
					os.path.join(os.path.dirname(__file__), 'libs')))

# XXX XXX XXX TEMPORARY FOR web2feed
sys.path.append(os.path.abspath('../web2feed'))

# ================= Common Configuration ==================

ROOT_URLCONF = 'sylph.urls'

TEMPLATE_DIRS = (os.path.join(os.path.abspath('.'), 'templates'),)
MEDIA_ROOT = os.path.join(os.path.abspath('.'), 'public_static')

APPEND_SLASH = True

# TODO: Utility to generate *ALL* absolute and relative system urls.

LOGIN_URL = '/system/login/'
LOGIN_REDIRECT_URL = '/'

MEDIA_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/media/'
ENDPOINT_URI = '/endpoint/'

FULL_BASE_URI = '' 		# The full URI (generated below)
FULL_ENDPOINT_URI = ''	# The full endpoint URI (generated below)

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
	'sylph.core.backend.context_processors.inject_settings',
	'sylph.core.backend.context_processors.owner_user_ref',
	#'sylph.core.backend.context_processors.ip_address',

	# Django Debug Toolbar
	#'debug_toolbar.middleware.DebugToolbarMiddleware',
)


# Middleware is applied in top-down order in request, reverse in response
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

	# Custom middlware
	'sylph.core.backend.middleware.EnsureInstalledMiddleware',
	'sylph.core.endpoint.middleware.EndpointExceptionHandlerMiddleware',
)

INSTALLED_APPS = (
	#'django.contrib.auth',			# Builtin user authentication
	'django.contrib.contenttypes',	# generic/dynamic querying w/o imports!! 
	#'django.contrib.admin',		# admin interface
	#'django.contrib.sessions',		# store data on visitors
	#'django.contrib.sites',		# SITE_ID, multiple django sites... 
	'django.contrib.humanize',		# 1 -> 'one', 10^6 -> '1.0 million', etc.

	# Django debug toolbar
	#'debug_toolbar',

	# Celery
	'djcelery', # Use 'celery' for older versions

	'sylph.core.endpoint',
	'sylph.core.resource',
	'sylph.core.node',
	'sylph.core.backend',
	'sylph.core.jobs',
	'sylph.core.subscription',
	#'sylph.core.frontend',

	'sylph.apps.post',
	'sylph.apps.blog',
	'sylph.apps.user',
	'sylph.apps.bootstrap',
	'sylph.apps.social',
)

# ================= Important DB Primary Keys =============

OUR_USER_PK = 1
OUR_NODE_PK = 2

# ================= Virtualization Helpers ================
"""
These functions make it easy to run multiple instances of Sylph to test
the communication abilities of the code. They allow binding of
different URLs and database schemas depending on which port the server
is told to run on:

	python manage.py runserver [port]

Port 8000 is considered the default.
"""

def get_port():
	"""Gets the port that python runserver was told to run on."""
	# FIXME: Very crude, only works if ONE argument is given!
	if len(sys.argv) < 3:
		return 8000
	try:
		return int(sys.argv[2])
	except ValueError:
		return 8000

def get_url(path = ""):
	"""Returns the URL with the port the server is running on,
	optionally with a path segment appended."""
	# FIXME: Not capable of binding different IP addresses!
	port = get_port()
	p = 'http://127.0.0.1%s/' % ("" if port == 80 else ":"+str(port))
	if not path or len(path) < 1:
		return p

	if path[0] == '/':
		p += path[1:]
	else:
		p += path

	if path[-1] != '/':
		p += '/'

	return p

def get_db(prefix = "sylph", port = None):
	"""Return the database name that the running instance will bind
	to. This varies based on the port django is told to run on."""
	if not port:
		port = get_port()
	if port == 8000:
		return prefix
	return prefix + str(port)

def get_rabbit_mq_vhost(prefix="sylph", port=None):
	"""These must be virtual hosts in /etc/hosts and installed in
	RabbitMQ. Essentially generated the same way database names are."""
	return get_db(prefix, port)


PORT = get_port() # XXX: Temporary for templates

FULL_BASE_URI = get_url()
FULL_ENDPOINT_URI = get_url('/endpoint/')


# ================= Import Specific Configs ===============

try:
    from settings_local import *
except ImportError:
    pass

