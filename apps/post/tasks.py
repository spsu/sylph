from celery.decorators import task
from models import *
from sylph.apps.social.models import User

from datetime import datetime
import hashlib

@task
def post_random_message():

	post = Post()

	post.datetime_created = datetime.today()
	post.uri = 'http://temp/post/' + \
						hashlib.md5(str(datetime.today())).hexdigest() 

	post.author = User.objects.get(id=1)

	post.title = 'asdf'
	post.contents = 'asdf'

	post.save()
