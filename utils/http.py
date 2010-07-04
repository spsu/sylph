from django.conf import settings

import httplib
from urllib import urlencode
from urlparse import urlparse

# This is the low-level wrapper around HTTP.
# The sylph protocol can be layered on top of this.
# XXX: Work in progress...

class Request(object):
	"""Perform a synchronous HTTP request.

		r = Request('http://slashdot.org/')
		result = r.download()
		print result.get_node_type()
	"""

	def __init__(self, uri, get={}, post={}, headers={}, timeout=10):
		self.uri = uri
		self.get = get
		self.post = post
		self.timeout = timeout
		self.headers = {
			'Accept': 'text/html,application/xhtml+xml,' + \
						'application/xml;q=0.9,*/*;q=0.8',
			# User agent and protocol
			'User-Agent': '%s (v%s/+http://github.com/echelon/sylph)' % \
										(settings.SOFTWARE_NAME,
										settings.SOFTWARE_VERSION),
			'X-Sylph-Protocol-Version': settings.PROTOCOL_VERSION,
		}

		# Add custom headers and/or overwrite defaults above
		for hk, hv in headers.iteritems():
			self.headers[hk] = hv

	def download(self, method='GET'):
		"""Perform the download.
		This is a synchronous request."""
		if self.post or method.upper() == 'POST':
			method = 'POST'
			post = urlencode(self.post)
			self.headers['Content-type'] = 'application/x-www-form-urlencoded'

		headers = {}
		status = 0
		body = ''

		try:
			uri = urlparse(self.uri)
			conn = httplib.HTTPConnection(uri.hostname, uri.port,
											timeout=self.timeout)
			if method == 'POST':
				conn.request(method, uri.path, params, self.headers)
			else:
				conn.request(method, uri.path, headers=self.headers)

			response = conn.getresponse()

			headers = {}
			for h in response.getheaders():
				headers[h[0]] = h[1]

			# XXX: Temporary debugging...
			status = response.status
			if response.status != 200:
				from sylph.utils.debug import parse_endpoint_trace
				print parse_endpoint_trace(response.read()) # XXX Debug trace
				raise Exception, "An exception occurred in comms."


			body = response.read()
			conn.close() # XXX/TODO: In the future, keep this open. 

		except:
			print "CONNECTION ERROR"
			pass

		return Response(self.uri, headers, status, body)

	# ============= Accessors / Mutators ==================

	def add_header(self, key, value):
		self.headers[key] = value

	def set_headers(self, headers):
		if type(headers) != dict:
			return
		self.headers = headers

	def get_headers(self):
		return self.headers

	def get_uri(self):
		return self.uri

# ================= Server Response =======================

class Response(object):
	"""Response from a download request."""

	def __init__(self, uri, headers={}, status=0, body=''):
		self.uri = uri
		self.headers = headers
		self.status = status
		self.body = body

	def is_sylph_node(self):
		"""Returns whether the page is a sylph node."""
		if 'X-Sylph-Protocol-Version' in self.headers:
			return True
		return False

	def is_feed(self):
		"""Returns whether the page is an RSS/Atom feed."""
		return None # TODO

	def is_webpage(self):
		"""Returns whether the page is a webpage via analysis
		of the payload"""
		return None # TODO

	def get_node_type(self):
		"""Return the type of node the page is."""
		if self.is_sylph_node():
			return 'sylph'
		elif self.is_feed():
			return 'feed'
		elif self.is_webpage():
			return 'webpage'
		return 'unknown'

	# ============= Accessors / etc. ======================

	def get_headers(self):
		return self.headers

	def get_uri(self):
		return self.uri

	def get_body(self):
		return self.body

	def get_status(self):
		return self.status

	def had_fatal_error(self):
		pass # TODO FIXME

