from django.conf import settings
from Response import Response
import hashlib
import httplib
import urllib
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup # for debug
from sylph.utils.termcolor import colored # for debug

try:
	from StringIO import StringIO
except:
	from cStringIO import StringIO

class Communicator(object):
	"""This class is for delivering data to another node. It
	negotiates HTTP and URL parsing for the user.

	If in the future we do multiple communication operations, use one
	Communicator per host.
	"""

	def __init__(self, uri="", timeout=10):

		# TODO: Multiple comms with host may need to be accomplished 
		# within a single session (keep alive parameter?)

		self.uri = urlparse(uri) if uri else ""
		self.timeout = timeout

	def set_uri(self, uri):
		"""Set the URI of the node we'll be accessing."""
		self.uri = urlparse(self.uri)

	def send_post(self, post_data={}):
		"""Send a dictionary of post data to the node.
		Return in a Response object."""
		if not self.uri:
			raise Exception, "Cannot send post without URI."

		params = urllib.urlencode(post_data)
		agent = '%s/%s' % (settings.SOFTWARE_NAME, settings.SOFTWARE_VERSION)
		headers = {
			'User-Agent': agent,
			'Content-type': 'application/x-www-form-urlencoded',
			'Accept': 'text/html,application/xhtml+xml,' + \
						'application/xml;q=0.9,*/*;q=0.8',
			#'X-Sylph-Protocol-Version': settings.PROTOCOL_VERSION,
		}

		hostname = self.uri.hostname
		port = 80 if not self.uri.port else self.uri.port
		path = self.uri.path

		try:
			conn = httplib.HTTPConnection(hostname, port, timeout=self.timeout)
			conn.request("POST", path, params, headers)
			response = conn.getresponse()

			print response

			if response.status != 200:
				print "Non-200 response!" # TODO DEBUG ONLY
				html = response.read()

				# Print Trace
				soup = BeautifulSoup(html)
				trace = soup.find('textarea', id='traceback_area').string
				trace = trace.split('Traceback:')[1]
				head = 'Remote Trace for %s:\n' % str(self.uri.geturl())
				print colored(head+trace, 'yellow')

				raise httplib.HTTPException, "Non-200 response"

			data = response.read()
			conn.close() # TODO: In future, keep connection in some cases
			return Response(data)

		except ValueError: #except httplib.HTTPException:
			conn.close() # TODO: In future, keep connection in some cases
			print "An exception occurred in comms." # TODO: Log this
			return None

	# TODO: Send wrapped RDF payloads
	#def send_payload(self, payload=None):
	#	# TODO: Payload will need get_mimetype() etc. 
	#	pass

