from celery.decorators import task
from models import *
from sylph.apps.user.models import User
from django.conf import settings

from datetime import datetime
import hashlib

@task
def post_random_message():
	print "test"
	post = Post()

	post.datetime_created = datetime.today()
	post.uri = 'http://temp/post/' + \
						hashlib.md5(str(datetime.today())).hexdigest()

	post.author = User.objects.get(pk=settings.OUR_USER_PK)

	post.title = 'asdf ' + str(settings.PORT) + 'sdf'
	post.contents = 'asdf'

	post.save()
