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
			#'X-Sylph-Protocol-Version': settings.PROTOCOL_VERSION,
		}

		hostname = self.endpoint_uri.hostname
		port = 80
		path = self.endpoint_uri.path
		if self.endpoint_uri.port:
			port = self.endpoint_uri.port

		try:
			conn = httplib.HTTPConnection(hostname, port, timeout=self.timeout)
			conn.request("POST", path, params, headers)
			response = conn.getresponse()

			if response.status != 200:
				print "Non-200 response!" # TODO DEBUG ONLY
				print response.read()[0:300]
				raise httplib.HTTPException, "Non-200 response"

		except httplib.HTTPException:
			conn.close() # TODO: In future, keep connection in some cases
			print "An exception occurred in comms." # TODO: Log this
			return False

		data = response.read()
		conn.close() # TODO: In future, keep connection in some cases

		return data

	# TODO: Send wrapped RDF payloads
	#def send_payload(self, payload=None):
	#	# TODO: Payload will need get_mimetype() etc. 
	#	pass

