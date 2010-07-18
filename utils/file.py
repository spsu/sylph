"""A few additional file operations."""

from django.conf import settings

import os
import shutil

def touch(fname, times = None):
	"""Imulates 'touch' for creating files, writing time."""
	# Taken from 
	# http://stackoverflow.com/questions/1158076/implement-touch-using-python
	with file(fname, 'a'):
		os.utime(fname, times)


def delete_uploads():
	"""Delete everything in the uploads directory."""
	# XXX: Deletes only directory paths that are numerical-only. 
	for p in os.listdir(settings.MEDIA_ROOT):
		path = os.path.join(settings.MEDIA_ROOT, p)
		if os.path.isdir(path) and p.isdigit():
			print "Deleting %s..." % path
			shutil.rmtree(path)


