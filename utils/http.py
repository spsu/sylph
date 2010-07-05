from django.conf import settings

import httplib
from urllib import urlencode
from urlparse import urlparse

"""
DON'T USE THIS DIRECTLY!

This is the low-level wrapper around making HTTP requests. (It's rather
pathetic at this point.) Sylph requests are built upon this at a higher
level. See 'comms.py'.
"""

class Request(object):
	"""Perform a synchronous HTTP request.

		r = Request('http://slashdot.org/')
		result = r.download()
		print result.get_node_type()
	"""

	def __init__(self, uri, get={}, post={}, headers={}, timeout=10,
					response_class=None):
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

		self.response_class = response_class

	# ============= Download ==============================

	def send(self, method='GET'):
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

		if not self.response_class:
			return Response.from_data(self.uri, headers, status, body)
		return self.response_class.from_data(self.uri, headers, status, body)

	# ============= HTTP Headers ==========================

	def add_header(self, key, value):
		self.headers[key] = value

	def add_headers(self, headers):
		"""Add a dictionary of headers. Overrides previous keys."""
		if type(headers) != dict:
			return
		for k, v in headers.iteritems():
			self.headers[k] = v

	def set_headers(self, headers):
		"""Set headers. Overrides all previous headers."""
		if type(headers) != dict:
			return
		self.headers = headers

	def get_headers(self):
		return self.headers

	# ============= GET dictionary ========================

	def add_get_var(self, key, value):
		self.get[key] = value

	def add_get_vars(self, get):
		if type(get) != dict:
			return
		for k, v in get.iteritems():
			self.get[k] = v

	def set_get(self, get):
		self.get = get

	def get_get(self):
		return self.get

	# ============= POST dictionary =======================

	def add_post_var(self, key, value):
		self.post[key] = value

	def add_post_vars(self, post):
		if type(post) != dict:
			return
		for k, v in post.iteritems():
			self.post[k] = v

	def set_post(self, post):
		self.post = post

	def get_post(self):
		return self.post

	# ============= Misc Accessors/Mutators ===============

	def get_uri(self):
		return self.uri

	def set_uri(self, uri):
		self.uri = uri

	def set_response_class(self, cls):
		self.response_class = cls

# ================= Server Response =======================

class Response(object):
	"""Response from a download request."""

	def __init__(self):
		"""Creates a blank response object."""
		self.uri = ''
		self.headers = {}
		self.status = 0
		self.body = ''

	@classmethod
	def from_data(cls, uri, headers={}, status=0, body=''):
		"""Create a Response object from the data provided.
		This type of factory constructor is required since Python
		does not allow method overloading"""
		response = cls()
		response.uri = uri
		response.headers = headers
		response.status = status
		response.body = body
		return response

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

