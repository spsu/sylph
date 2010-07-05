from sylph.utils.http import Request, Response
from sylph.utils.data.RdfSerializer import RdfSerializer

class SylphRequest(object):
	"""Make a Sylph Request to another node. This is built on top of
	the basic HTTP library."""

	def __init__(self, uri, timeout=10, serializer='RDF'):

		self.request = Request(uri, timeout=timeout)
		self.serializer = None
		self.payload = []

	def send(self):
		"""Perform the communication. We only serialize data at this
		point."""
		if self.payload:
			self.__add_payload_to_request()

		response = None
		try:
			response = self.request.send()
		except Exception as e:
			print e # XXX DEBUG
			pass

		if self.payload:
			self.__remove_payload_from_request()

		return SylphResponse(response)

	def add(self, transportable):
		"""Add a model object or QuerySet to the payload in
		preparation to be sent to the remote node."""
		self.payload.append(transportable)

	def __add_payload_to_request(self):
		"""Add the object payload to the request. This performs the
		serialization work."""
		if not self.payload:
			return

		serialize_format = None # TODO: Just make a serializer method
		if not self.serializer:
			self.serializer = RdfSerializer()
			serialize_format = 'RDF/XML'

		# We serialize only when about to be sent...
		for obj in self.payload:
			self.serializer.add(obj)

		# TODO: should be serializer.serialize() !!
		self.request.add_post_var('data', self.serializer.to_rdf())
		self.request.add_post_var('format', serialize_format)

		# TODO: Remove data from the serializer...
		# self.serializer.flush()

	def __remove_payload_from_request(self):
		"""Remove the payload from the request."""
		# XXX/TODO: Breaks abstraction...
		del self.request.post['data']
		del self.request.post['format']

	# TODO: Set an alternate serializer (eg. JSON)
	#def set_serializer(self, serializer):
	#	"""Can take string name or object, but will flush the 
	#	serialier of any existing data."""
	#	pass

# ============ Response =========================

# XXX: This should represent all responses: Sylph, Webpage, etc.
class SylphResponse(Response):

	def __init__(self, django_response=None):
		# member vars: uri, headers, status, body 
		super(SylphResponse, self).__init__()



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

	def get_protocol_version(self):
		pass

	def get_software_name(self):
		pass

	def get_software_version(self):
		pass


