"""A few additional file operations."""

import os

def touch(fname, times = None):
	"""Touch a file.""" 
	# Taken from 
	# http://stackoverflow.com/questions/1158076/implement-touch-using-python
	with file(fname, 'a'):
		os.utime(fname, times)

