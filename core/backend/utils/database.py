from django.core import management
from django.db import connection

from sylph.core.resource.models import Resource

# TODO: perhaps mv utilities.py db_utilities.py or similar..


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
		print "Models not found, syncing database..."
		sync_database()


# ============ Drop/Reset Database ==============

def reset_database():
	"""Resets the django database, dropping and re-adding each table."""
	# MODIFIED FROM CODE FOUND AT:
	# http://groups.google.com/group/django-users/browse_thread/
	# thread/456539bfad0c8a93/f7f57f3cc75eec5b?lnk=raot

	cursor = connection.cursor()
	saveTables = [] # List of tables to spare execution

	currentTables = connection.introspection.table_names()

	for table in currentTables:
		if table not in saveTables:
			try:
				cursor.execute("drop table %s" % table)
			except Exception,e:
				raise e

	management.call_command('syncdb', interactive=False) 
	management.call_command('loaddata', 'fixtures/initial_configs.json', 
					verbosity=1, interactive=False) 
	management.call_command('loaddata', 'fixtures/initial_node.json', 
					verbosity=1, interactive=False) 
	management.call_command('loaddata', 'fixtures/initial_social.json', 
					verbosity=1, interactive=False) 


