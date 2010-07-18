from django.core import management
from django.db import connection
from django.conf import settings

from sylph.core.resource.models import Resource
from sylph.core.node.models import Node

import os
from glob import glob

# TODO: perhaps mv utilities.py db_utilities.py or similar..

# ============ Sync Database ====================

def sync_database():
	"""Simple call to sync the database."""
	management.call_command('syncdb', interactive=False)

# ============ Load fixtures ====================

def load_fixtures():
	"""Load the fixtures into the database."""
	fixture_dir = 'fixtures'

	for f in glob(os.path.join(fixture_dir, '*.json')):
		management.call_command('loaddata', f, verbosity=1, 
				interactive=False)

# ============ Sync On Empty Schema =============

def sync_database_on_error():
	"""Syncs/Loads fixtures"""
	if _database_has_errors():
		sync_database()
		load_fixtures()

def reset_database_on_error():
	"""Resets database."""
	if _database_has_errors():
		reset_database()

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

	# Reload everything to a pristine state... 
	drop_tables()
	sync_database()
	load_fixtures()

# ============ Detect db errors =================

def _database_error_check():
	"""Heuristic(s) to check if database has errors."""
	err = False
	try:
		Resource.objects.get(pk=1)
		Resource.objects.get(pk=2)
	except Resource.DoesNotExist:
		err = True

	# TODO: add more checks
	return err

