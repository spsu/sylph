from Message import Message
from sylph.utils.data.RdfParser import RdfParser

class Response(Message):
	"""
	Response Messages wrap the response from HTTP communications.
	They will be used to extract RDF.
	Typically not instantiated by user code.
	"""
	def __init__(self, raw_data):
		super(Response, self).__init__()

		self.raw_data = raw_data
		self.parser = None

	# ============= High-level API ========================

	def extract(self, type):
		"""Extract all data of a known type.
		eg. Node, Resource, Post, etc."""
		# XXX: This is not a nice interface / good practice. 
		if not self.raw_data:
			raise Exception, "There's nothing to extract."
		if not self.parser:
			self.parser = RdfParser(self.raw_data)
		return self.parser.extract(type)

	# ============= Lower-level API =======================
