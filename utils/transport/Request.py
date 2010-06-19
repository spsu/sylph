from Message import Message
from Communicator import Communicator
from sylph.utils.data.RdfSerializer import RdfSerializer

class Request(Message):

	def __init__(self):
		super(Request, self).__init__(self)

		self.communicator = None
		self.destination = None
		self.serializer = None

	# ============= High-level API ========================

	def add(self, transportable):
		"""Add a model object or QuerySet to the serializer in
		preparation to be sent to the remote node."""
		#XXX: Ideally, it isn't the job of this class to know the 
		#	  implementation details behind storing this info.
		if not self.serializer:
			self.serializer = RdfSerializer()
		self.serializer.add(transportable)

	def get_serialized(self):
		"""Get the output of the models added thus far."""
		if not self.serializer:
			raise Exception, "No data to output!"
		return self.serializer.to_rdf()


	# XXX: DATA SHOULDN'T HAVE COMM PARAMS!!! WTF?! DECOUPLE!!
	"""
	def set_destination(self):
		if not self.communicator:
			self.communicator = Communicator()
		self.communicator.set_uri(destination)

	def send(self, destination=None, dispatch='ping'):
		if not self.communicator:
			self.communicator = Communicator()
		if not destination:
			destination = self.destination
		self.communicator.set_uri(destination)
		self.return_data = self.communicator.send_post({'dispatch': dispatch})
		return self.return_data


	def send_async(self, destination, dispatch='ping'):
		pass # TODO

	"""

	# ============= Lower-level API =======================

	def get_communicator(self):
		"""Get a reference to the communicator."""
		if not self.communicator:
			self.communicator = Communicator()
		return self.communicator

	def set_communicator(self, communicator):
		"""Set a communicator for the class."""
		if type(communicator) != Communicator:
			raise Exception, "Must supply Communicator object."
		ret = self.communicator
		self.communicator = communicator
		return ret

	def get_serializer(self):
		"""Get a reference to the serializer held by the Payload.
		If none, create one now."""
		if not self.serializer:
			self.serializer = RdfSerializer()
		return self.serializer

	def set_serializer(self, serializer):
		"""Set the serializer object for the Request. If one already
		exists, return it after setting the new one."""
		if type(serializer) != RdfSerializer:
			raise Exception, "Must supply serializer object."
		ret = self.serializer
		self.serializer = serializer
		return ret

