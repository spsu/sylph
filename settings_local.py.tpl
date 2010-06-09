# Local settings

from settings import MEDIA_URL, get_port, get_url, get_db, get_rabbit_mq_vhost

DATABASE_ENGINE = 'mysql'
DATABASE_NAME = None # defined later... 
DATABASE_USER = 'DB_USER'
DATABASE_PASSWORD = 'DB_PASS'
DATABASE_HOST = ''
DATABASE_PORT = ''

CELERY_RESULT_BACKEND = "database"

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_VHOST = get_rabbit_mq_vhost()
BROKER_USER = "sylph" # TODO: More than one user?
BROKER_PASSWORD = "PASSWORD"

# For spawning on different databases if a different port is used.
__portList = [7000, 9000, 10000]
if get_port() in __portList:
	DATABASE_NAME = get_db('sylph')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS

SECRET_KEY = 'SOME UNIQUE STRING MORE RANDOM THAN THIS'


