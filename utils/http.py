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

class Message(object):
	"""A message object is a store for basic information sent over HTTP
	This represents both Request and Response, as it's basically the
	same information store as accessed by both endpoints.
	"""

	# TODO: GET isn't supported: It won't be stripped from URL or placed there!
	def __init__(self, uri='', get={}, post={}, headers={}, body=''):
		self.uri = uri
		self.get = get
		self.post = post
		self.headers = headers
		self.body = body

	# ============= URI/Body ==============================

	def get_uri(self):
		return self.uri

	def set_uri(self, uri):
		self.uri = uri

	def get_body(self):
		return self.body

	def set_body(self, body):
		self.body = body

	# ============= HTTP Headers ==========================

	def add_header(self, key, value):
		self.headers[key] = value

	def add_headers(self, headers):
		if type(headers) != dict:
			return
		for k, v in headers.iteritems():
			self.headers[k] = v

	def set_headers(self, headers):
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

# ============ Subtypes =========================

class Request(Message):
	pass

class Response(Message):
	pass

# ============ Communication Functions ====================

def get(uri, timeout=10, response_class=Response):
	"""Simple fetch of a URI. No request message payload"""
	return send(Request(), uri, 'GET', timeout, response_class)

def send(message, uri=None, method='GET', timeout=10, response_class=Response):
	"""Send a Request Message and get a Response Message."""
	if not uri:
		uri = message.uri

	outheaders = {
		'Accept': 'text/html,application/xhtml+xml,' + \
					'application/xml;q=0.9,*/*;q=0.8',
		# User agent and protocol
		'User-Agent': '%s (v%s/+http://github.com/echelon/sylph)' % \
								(settings.SOFTWARE_NAME,
								settings.SOFTWARE_VERSION),
		'X-Sylph-Protocol-Version': settings.PROTOCOL_VERSION,
	}

	# Add custom headers and/or overwrite defaults above
	for hk, hv in message.headers.iteritems():
		outheaders[hk] = hv

	post = None
	if message.post or method.upper() == 'POST':
		method = 'POST'
		post = urlencode(messsage.post)
		outheaders['Content-type'] = 'application/x-www-form-urlencoded'

	# Use the appropriate message store
	if response_class:
		response = response_class(uri)
	else:
		response = Response(uri)

	try:
		uri = urlparse(uri)
		conn = httplib.HTTPConnection(uri.hostname, uri.port, timeout=timeout)
		if method == 'POST':
			conn.request(method, uri.path, post, outheaders)
		else:
			conn.request(method, uri.path, headers=outheaders)

		resp = conn.getresponse()

		# TODO: Handle redirects...
		# Allow user to select between follow/nofollow, plus max redirect cnt

		for h in resp.getheaders():
			response.headers[h[0]] = h[1]

		# XXX: Temporary debugging...
		response.status = resp.status
		if response.status != 200:
			from sylph.utils.debug import parse_endpoint_trace
			print parse_endpoint_trace(resp.read()) # XXX Debug trace
			raise Exception, "An exception occurred in comms."

		response.body = resp.read()
		conn.close() # XXX/TODO: In the future, keep this open. 

	except Exception as e:
		print "CONNECTION ERROR"
		print e
		pass

	return response

