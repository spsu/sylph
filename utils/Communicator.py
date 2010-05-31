from django.conf import settings
import hashlib
import httplib
import urllib
from urlparse import urlparse

class Communicator(object):
	"""This class is for delivering data to another endpoint. It 
	negotiates HTTP and URL parsing for the user."""

	def __init__(self, endpoint_uri, timeout=10):

		# TODO: Multiple comms with host may need to be accomplished 
		# within a single session (keep alive parameter?)

		self.endpoint_uri = urlparse(endpoint_uri) 
		self.timeout = timeout
		
	def send_post(self, post_data={}):
		"""Send a dictionary of post data to the endpoint."""
		params = urllib.urlencode(post_data)
		agent = '%s/%s' % (settings.SOFTWARE_NAME, settings.SOFTWARE_VERSION)
		headers = {
			'User-Agent': agent,
			'Content-type': 'application/x-www-form-urlencoded',
			'Accept': 'text/html,application/xhtml+xml,' + \
					  'application/xml;q=0.9,*/*;q=0.8',
			'X-Sylph-Protocol-Version': settings.PROTOCOL_VERSION,
		}

		hostname = self.endpoint_uri.hostname
		port = self.endpoint_uri.port
		path = self.endpoint_uri.path

		conn = httplib.HTTPConnection(hostname, port, timeout=self.timeout)
		response = conn.request("POST", path, params, headers)

		data = response.read()
		conn.close() # TODO: In future, keep connection in some cases

	# TODO: Send wrapped RDF payloads
	#def send_payload(self, payload=None):
	#	# TODO: Payload will need get_mimetype() etc. 
	#	pass

