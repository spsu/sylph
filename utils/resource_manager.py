from sylph.utils import http
from sylph.utils import comms
from sylph.utils.uri import hashless

from sylph.core.resource.models import Resource
from sylph.apps.media.models import Image

from web2feed import Web2Feed

"""
Resource Manager is a very high level downloader for Resources.
"""

# XXX: Doesn't work except for images
def obtain(uri):
	"""Obtain the resource at the URI."""
	uri = hashless(uri)
	res = None
	try:
		res = Resource.objects.get(uri=uri)
		return # XXX: Don't modify existing.
	except Resource.DoesNotExist:
		pass

	message = comms.get(uri)

	# XXX TODO: Handle resources.
	if message.is_image():
		res = Image.new_from_message(message, save=True)

	elif message.is_html():
		# TODO/XXX: Try web2feed extraction
		web = Web2Feed(uri)
		web.set_contents(message.get_body)
		feed = web.get_feed()
		# XXX: TODO

	#typ = message.get_content_type()
	#if typ in ['image/jpeg', 'image/png', 'image/gif']:
	#	res = Image.new_from_message(message, save=True)	
	return res

def delete(uri):
	pass



