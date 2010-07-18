from sylph.utils.http import Message
from sylph.utils.http import send as http_send
from sylph.utils.http import django_receive as http_django_receive
from sylph.utils.data.RdfSerializer import RdfSerializer
from sylph.utils.data.RdfParser import RdfParser

# TODO: Parser should be more decoupled.
# TODO: Alternative parser/serializers, eg. JSON
# TODO**: Mechanism to determine what the type of resource is!

class SylphMessage(Message):
	"""
	Message is a content store relayed between two endpoints.

	Sylph messages are an extension of the lower-level HTTP Message
	store. They add the ability to store Models or QuerySets as well as
	determine what the type of the sender or receiver is based on
	analysis of the headers or content.
	"""

	def __init__(self, uri=''): # TODO: Fix/standardize args
		super(SylphMessage, self).__init__(uri)

		# High-level serialized and parsed info (respectively)
		self.payload = []
		self.extracted = None # TODO

		# Serializer/Parser objects.
		self.serializer = None
		self.parser = None

	# ============= Add/Get Payloads ======================

	def add(self, transportable):
		"""Add a model object or QuerySet to the payload in preparation
		to be sent to the remote node."""
		self.payload.append(transportable)

	def extract(self, type):
		"""Extract all data of a known type. (eg. Node, User, etc.)"""
		# XXX: This is not a nice interface / good practice.
		# TODO: See self.extracted wrt. self.payload. Make them analogous for
		# the two modalities of transfer. (response->extracted)
		if not self.body:
			return None # Nothing to extract
		if not self.parser:
			# XXX/TODO: Parser shouldn't contain content!!! BAD! REUSE IS GOOD!
			self.parser = RdfParser(self.body)
		return self.parser.extract(type) # XXX: BAD

	# XXX/TODO: If something new is added to payload, **mark headers stale** instead
	def _sync(self):
		if self.payload:
			self.__add_payload_to_headers()
		elif self.body:
			pass # TODO: Try to parse out all content to self.extracted!

	def _unsync(self):
		if self.payload:
			self.__remove_payload_from_headers()
		elif self.body:
			pass # TODO: Read above todo (remove from self.extracted?)

	def __add_payload_to_headers(self):
		"""Add the object payload to the message. This performs the
		serialization work."""
		if not self.payload:
			return

		serialize_format = None # TODO: Convert to serializer method
		if not self.serializer:
			self.serializer = RdfSerializer()
			serialize_format = 'RDF/XML'

		# We serialize only when about to be sent...
		for obj in self.payload:
			self.serializer.add(obj)

		# TODO: should be serializer.serialize() !!
		self.add_post_var('data', self.serializer.to_rdf())
		self.add_post_var('format', serialize_format)

		# TODO: Remove data from the serializer to keep state pure
		# self.serializer.flush()

	def __remove_payload_from_headers(self):
		"""Remove the payload from the message."""
		del self.post['data']
		del self.post['format']

	# TODO: Set an alternate serializer (eg. JSON)
	#def set_serializer(self, serializer):
	#	"""Can take string name or object, but will flush the 
	#	serialier of any existing data."""
	#	pass

	# ============= Content/Node Type Analysis ============

	def is_sylph_node(self):
		"""Returns whether the sender/receiver is a sylph node."""
		if 'X-Sylph-Protocol-Version' in self.headers:
			return True
		return False

	def is_feed(self): # TODO
		"""Returns whether the content is an RSS/Atom feed."""
		return None

	def is_webpage(self): # TODO
		"""Returns whether the content is a webpage."""
		# This is going to be imperfect...
		# First check the headers 
		mimetypes = ['text/html', 'application/xhtml+xml']
		if 'Content-Type' in self.headers and \
			self.headers['Content-Type'] in mimetypes:
				return True
		# This is a really poor heuristic...
		if len(self.body) > 100 and "<html" in self.body[0:100]:
			return True
		return False

	def get_node_type(self): # TODO: Depends on above.
		"""Return the type of node the page is."""
		if self.is_sylph_node():
			return 'sylph'
		elif self.is_feed():
			return 'feed'
		elif self.is_webpage():
			return 'webpage'
		return 'unknown'

	def get_protocol_version(self): # TODO
		"""Gets from headers."""
		pass

	def get_software_name(self): # TODO
		"""Gets from headers."""
		pass

	def get_software_version(self): # TODO
		"""Gets from headers."""
		pass

# ============ Communications Methods ===========

def get(uri, timeout=10, response_class=SylphMessage):
	"""Simple fetch of a URI. No request message payload"""
	return http_send(SylphMessage(), uri, 'GET', timeout, response_class)

def send(message, uri=None, method='GET', timeout=10, response_class=SylphMessage):
	"""Send a Request Message and get a Response Message."""
	message._sync()
	response = http_send(message, uri, method, timeout, response_class)
	message._unsync()
	return response

def django_receive(request):
	return http_django_receive(request)

# XXX/TODO: Once fixed, this belongs in http.py
def django_respond(message):
	"""Send a message over as the HTTP response from a django view."""
	from django.http import HttpResponse

	# XXX XXX XXX: This is very bad/messy...
	message._sync()
	data = message.headers['data']
	message._unsync()

	# TODO: Mimetype should be based on serialization format
	return HttpResponse(data, mimetype='text/plain')

