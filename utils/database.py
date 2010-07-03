from django.core import management
from django.db import connection
from django.conf import settings

from sylph.core.resource.models import Resource
from sylph.core.node.models import Node

# ============ Get all models ===================

def get_all_models():
	"""A (hopefully) maintained list of all models.
	This must be kept for deleting manually on Google App Engine."""
	from sylph.core.backend.models import BackendConfig
	from sylph.core.node.models import Node
	from sylph.core.resource.models import Resource
	from sylph.core.resource.models import ResourceTree
	from sylph.core.resource.models import ResourceType
	from sylph.core.subscription.models import Subscription
	from sylph.apps.blog.models import BlogItem
	from sylph.apps.post.models import Post
	from sylph.apps.user.models import User
	from sylph.apps.user.models import UserEmail
	from sylph.apps.social.models import Knows
	from sylph.apps.social.models import ProfilePost

	return [
				BackendConfig,
				Node,
				Resource, ResourceTree, ResourceType,
				Subscription,
				BlogItem,
				Post,
				User, UserEmail,
				Knows, ProfilePost
	]

# ============ Sync Database ====================

def sync_database():
	"""Simple call to sync the database."""
	management.call_command('syncdb', interactive=False)

# ============ Sync On Empty Schema =============

def sync_empty_database():
	"""Calls sync database if the Resource relation is found not to exist."""
	# This is a lame attempt at catching an empty database. 
	try:
		r = len(Resource.objects.all())

	except Exception: # XXX: Not exactly sure where 'ProgrammingError' is from.
		# XXX BLAME: commit 50dd074c5972971eeaa3d7be59b65b3903f85ed1
		print "Models not found, syncing database..."
		sync_database()

# ============ Drop/Reset Database ==============

def reset_database():
	"""Resets the django database, dropping and re-adding each table."""

	def drop_tables(save_tables=[]):
		"""Drop database tables not in save_tables
		Not to be used on non-relational backends.
		FROM CODE FOUND AT:
		http://groups.google.com/group/django-users/browse_thread/
		thread/456539bfad0c8a93/f7f57f3cc75eec5b?lnk=raot
		"""
		cursor = connection.cursor()
		cur_tables = connection.introspection.table_names()

		for table in cur_tables:
			if table in save_tables:
				continue
			try:
				cursor.execute("drop table %s" % table)
			except Exception,e:
				raise e


	def delete_each_manually():
		"""Crude Google App Engine delete for resources."""
		# XXX/TODO: This won't work if there are over 1000 resources!

		for model in get_all_models():
			try:
				objs = model.objects.all()
				ln = len(objs)
				for o in objs:
					o.delete()
				print "%s had %d objects deleted" % (str(model), ln)
			except Exception as e:
				print e
				continue

	if settings.IS_GOOGLE_APP_ENGINE:
		delete_each_manually()
	else:
		drop_tables()

	management.call_command('syncdb', interactive=False)
	management.call_command('loaddata', 'fixtures/initial_configs.json',
					verbosity=1, interactive=False)
	management.call_command('loaddata', 'fixtures/initial_node.json',
					verbosity=1, interactive=False)
	management.call_command('loaddata', 'fixtures/initial_user.json',
					verbosity=1, interactive=False)

