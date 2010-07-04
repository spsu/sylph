from django.conf import settings
import uuid

def clean(uri): # TODO
	"""
	Clean URIs by mapping them onto a standard resource form.
		* Remove trailing hash
		* TODO: Remove query string?
	"""
	pass # TODO

def hashless(uri):
	"""Remove any trailing hash from a URI."""
	return uri.split('#')[0]

def generate_uuid(path=''):
	"""Generate a unique UUID uri for a resource."""
	uri = settings.FULL_BASE_URI
	uri = __append_path(uri, path)
	return __append_path(uri, str(uuid.uuid4()))

def generate_md5(content, base=None): # TODO
	pass # TODO

# ============ Private, Non-API ===========================

def __append_path(uri_base, path_append):
	"""Helper function to append a path intelligently to a base URI."""
	p = uri_base
	if not path_append or len(path_append) < 1:
		return p

	if path_append[0] == '/':
		p += path_append[1:]
	else:
		p += path_append

	if path_append[-1] != '/':
		p += '/'

	return p

