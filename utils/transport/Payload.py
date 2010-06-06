from Communicator import Communicator
from RdfParser import RdfParser
from RdfSerializer import RdfSerializer

class Payload(object):

	# TODO/XXX: This class is a mess!

	def __init__(self):
		"""Blank CTOR."""
		# Outgoing
		self.communicator = None
		self.destination = None
		self.serializer = None
		# Incoming
		self.return_data = None
		self.parser = None

	# ============= High-level Payload API ================

	def add(self, transportable):
		"""Add a model object or QuerySet to the serializer in 
		preparation to be sent to the remote node."""
		if not self.serializer:
			self.serializer = RdfSerializer()
		self.serializer.add(transportable)

	def set_destination(self):
		if not self.communicator:
			self.communicator = Communicator()
		self.communicator.set_uri(destination)

	def send(self, destination=None, dispatch='ping'):
		"""Send data to the remote node and get return data."""
		if not self.communicator:
			self.communicator = Communicator()
		if not destination:
			destination = self.destination
		self.communicator.set_uri(destination)
		self.return_data = self.communicator.send_post({'dispatch': dispatch})
		return self.return_data

	def send_async(self, destination, dispatch='ping'):
		pass # TODO

	def extract(self, type):
		"""Extract data"""
		if not self.return_data:
			raise Exception, "There's nothing to extract."
		if not self.parser:
			self.parser = RdfParser(self.return_data)
		return self.parser.extract(type)

	def get_output(self):
		"""Get the output of the models added thus far."""
		if not self.serializer:
			raise Exception, "No data to output!"
		return self.serializer.to_rdf()


	# ============= Lower-level Payload API ===============

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
		"""Set the serializer object for the Payload. If one already
		exists, return it after setting the new one."""
		if type(serializer) != RdfSerializer:
			raise Exception, "Must supply serializer object."
		ret = self.serializer
		self.serializer = serializer
		return ret


