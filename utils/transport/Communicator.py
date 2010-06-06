from django.conf import settings
import hashlib
import httplib
import urllib
from urlparse import urlparse

class Communicator(object):
	"""This class is for delivering data to another endpoint. It 
	negotiates HTTP and URL parsing for the user."""

	def __init__(self, endpoint_uri="", timeout=10):

		# TODO: Multiple comms with host may need to be accomplished 
		# within a single session (keep alive parameter?)

		self.endpoint_uri = endpoint_uri
		self.timeout = timeout

	def set_uri(self, uri):
		"""Set the URI of the endpoint we'll be accessing."""
		self.endpoint_uri = uri
		
	def send_post(self, post_data={}, destination=None):
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

		uri = destination if destination else self.endpoint_uri
		uri = urlparse(uri)

		hostname = uri.hostname
		port = 80 if not uri.port else uri.port
		path = uri.path

		try:
			conn = httplib.HTTPConnection(hostname, port, timeout=self.timeout)
			conn.request("POST", path, params, headers)
			response = conn.getresponse()

			print response

			if response.status != 200:
				print "Non-200 response!" # TODO DEBUG ONLY
				print response.read()[0:300]
				raise httplib.HTTPException, "Non-200 response"

			data = response.read()
			conn.close() # TODO: In future, keep connection in some cases
			return data

		except: #except httplib.HTTPException:
			conn.close() # TODO: In future, keep connection in some cases
			print "An exception occurred in comms." # TODO: Log this
			return False

	# TODO: Send wrapped RDF payloads
	#def send_payload(self, payload=None):
	#	# TODO: Payload will need get_mimetype() etc. 
	#	pass

