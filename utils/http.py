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

# TODO: Cookies
# TODO: File transfers
# TODO: GET - proper support
# TODO: Handle redirects -- will report failure on redirects!
#       NOTE: Node/Resource location should be updated?
# TODO: Connection pool (keepalive, etc.)
# TODO: Error handling/store

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
		self._mimetype = None # cached

	# ============= High-level ============================

	def get_content_type(self):
		"""Heuristic to guess content type.
		First checks headers, then magic number, then XML/HTML meta."""
		# TODO: cache invalidation if body changes
		if self._mimetype:
			return self._mimetype

		mimetype = ''
		for h, v in self.headers.iteritems():
			if 'content-type' == h.lower():
				mimetype = v
				break

		if mimetype:
			if ';' not in mimetype:
				self._mimetype = mimetype.strip()
			else:
				self._mimetype = mimetype.split(';')[0].strip()
			return self._mimetype

		if len(self.body) == 0:
			self._mimetype = 'application/x-empty'
			return self._mimetype

		# XXX: This is NOT cross-platform:
		if os.name == 'posix':
			try:
				import magic
				self._mimetype = magic.from_buffer(self.body, mime=True)
				return self._mimetype
			except:
				pass
	
		self._mimetype = 'unknown'
		return self._mimetype

	def is_image(self):
		"""If the body contains an image."""
		imgs = ['image/jpeg', 'image/png', 'image/gif']
		return self.get_content_type() in imgs

	def is_html(self):
		html_types = ['text/html', 'application/xhtml+xml']
		return self.get_content_types() in html_types

	# ============= Errors ================================

	# TODO: There can be an error store that takes on errors on both ends as well
	# as during communication itself.

	def has_errors(self):
		return False # XXX/TODO

	def set_error(self, key, val): # TODO: this and etc. methods
		pass

	# ============= URI/Body ==============================

	def get_uri(self):
		return self.uri

	def set_uri(self, uri):
		self.uri = uri

	def get_body(self):
		return self.body

	def set_body(self, body):
		self._mimetype = None
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
		self._mimetype = None # in case 'content-type'
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

	def set_post(self, *args):
		if len(args) == 1 and type(args[0]) == dict:
			self.post = args[0]
		elif len(args) == 2:
			self.post[args[0]] = args[1]

	def get_post(self, *args):
		if len(args) == 0:
			return self.post
		elif len(args) == 1:
			return self.post[args[0]]
		else:
			raise Exception, "Message.get_post(): Too many arguments"

# ============ Communication Functions ====================

def get(uri, timeout=10, response_class=Message):
	"""Simple fetch of a URI. No request message payload"""
	return send(Message(), uri, 'GET', timeout, response_class)

def send(message, uri=None, method='GET', timeout=10, response_class=Message):
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
		post = urlencode(message.post)
		outheaders['Content-Type'] = 'application/x-www-form-urlencoded'

	# Use the appropriate message store
	if response_class:
		response = response_class()
		response.set_uri(uri)
	else:
		response = Message(uri)

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
			print "Response is not 200 OK!"
			print response.status
			print response.headers
			from sylph.utils.debug import parse_endpoint_trace
			print parse_endpoint_trace(resp.read(), 'TODO:URI') # XXX Debug trace
			raise Exception, "An exception occurred in comms."

		response.body = resp.read()
		conn.close() # XXX/TODO: In the future, keep this open. 

	except Exception:
		print "CONNECTION ERROR"

	return response

def django_receive(request):
	"""Process a Django request object into a message we can use."""
	ret = Message()

	get = {}
	for k, v in request.GET:
		if type(v) == list: # XXX: Why is django doing this?
			v = v[0]
		get[k] = v

	post = {}
	for k, v in request.POST.iteritems():
		if type(v) == list: # XXX: Why is django doing this?
			v = v[0]
		post[k] = v

	# Django screws with the headers... **and** stores them in bad place!
	headers = {}
	for k, v in request.META.iteritems():
		# XXX/TODO: This skips a few headers that are arbitrarily not 'HTTP_'
		if len(k) < 5 or k[0:5] != 'HTTP_':
			continue
		nk = k[5:] # remove the 'HTTP_'
		if nk != k.replace('HTTP_', ''):
			nk = k
		# Fix case (Assume it is always Some-Http-Method)
		nk = nk.replace('_', '-').lower().title()
		headers[nk] = v

	ret.set_get(get)
	ret.set_post(post)
	ret.set_headers(headers)

	# TODO: Cookies, Files... anything else?
	return ret

