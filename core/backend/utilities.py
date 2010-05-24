from django.core import management
from django.db import connection

from sylph.core.endpoint.models import Resource

def sync_database():
	"""Simple call to sync the database."""
	management.call_command('syncdb', interactive=False) 

def sync_empty_database():
	"""Calls sync database if the Resource relation is found not to exist."""
	# This is a lame attempt at catching an empty database. 
	try:
		r = len(Resource.objects.all())

	except Exception: # XXX: Not exactly sure where 'ProgrammingError' is from.
		print "Models not found, syncing database..."
		sync_database()

def reset_database():
	"""Resets the django database, dropping and re-adding each table."""
	# CODE FROM 
	# http://groups.google.com/group/django-users/browse_thread/
	# thread/456539bfad0c8a93/f7f57f3cc75eec5b?lnk=raot

	cursor = connection.cursor()
	saveTables = [] # Tables to save

	currentTables = connection.introspection.table_names()

	for table in currentTables:
		if table not in saveTables:
			try:
				cursor.execute("drop table %s" % table)
			except Exception,e:
				raise e

	management.call_command('syncdb', interactive=False) 


