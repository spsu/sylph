class Intermediary(object):
	"""
	Intermediary objects represent the data stores that applications will 
	pass around to communicate and receive information. 

	Simplified Communication model:
		NODE_A <-> Intermediary <-> RdfPayload <-> Intermediary <-> NODE_B
	"""

	def __init__(self):

		# Define the origin.
		# TODO: CONCENTRATE ON THESE SEMANTICS LATER
		self.originHeaders = []

		# Define where the payload is going
		self.destHeaders = []

		# A unique Resource that defines the semantics of the operation. 
		self.communicationType = '' # XXX: CONCENTRATE ON THIS.

		# RDF or media or something. 
		self.data = [] # TODO: Not an appropriate store


	def addOriginHeader(self, header_or_key, value = None):
		"""Set an origin header with object or values."""
		header = header_or_key
		if type(header_or_key) == str:
			header = Header(header_or_key, value)

		for i in range(len(self.originHeaders)):
			if header.key == self.originHeaders[i].key:
				self.originHeaders[i] = header
				return

		self.originHeaders += header

	def addDestHeader(self, header_or_key, value = None):
		"""Set an origin header with object or values."""
		header = header_or_key
		if type(header_or_key) == str:
			header = Header(header_or_key, value)

		for i in range(len(self.destHeaders)):
			if header.key == self.destHeaders[i].key:
				self.destHeaders[i] = header
				return

		self.originHeaders += header

	def getPayload(self):
		"""Gets the RdfPayload of the current intermediary."""
		from RdfPayload import RdfPayload
		return RdfPayload(self)
