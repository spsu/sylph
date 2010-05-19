from django.core import management
from django.db import connection

def resetDatabase():
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

	management.call_command('syncdb') 
