# XXX: Probably not the final place for context processors to reside
from django.conf import settings as _settings

def ip_address(request):
	"""Return IP address (from Django docs)"""
	return {'ip_address': request.META['REMOTE_ADDR']}

def settings(request):
	"""Allows use of Django settings in templates""" # XXX: is this wise?
	return {'settings': _settings }
