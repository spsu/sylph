from sylph.core.endpoint.models import Resource

# Django
from django.db.models.query import QuerySet

# RDF Lib
import rdflib
from rdflib.Graph import ConjunctiveGraph as Graph
from rdflib import Namespace, URIRef, Literal, BNode, RDF
#from rdflib.store import Store

# Describes an Incoming or Outgoing payload
# Great, but this HAS TO BE TURNED INTO POSTDATA. 

# TODO: Make it possible to "finalize" the intermediary at construction,
# making it impossible to alter the data contained (This is for receivers.)

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


	# ============= Add Result ============================

	def addResult(self, queryRet):
		"""Add a query result to the intermediary."""
		if type(queryRet) not in [list, tuple, QuerySet]:
			if not isinstance(queryRet, Resource):
				raise TypeError, "Query Result must be a Resource!\n"

			mod = self.ModelData(queryRet)
			self.data.append(mod)
			return 

		if type(queryRet) in [list, tuple, QuerySet]:
			for qr in queryRet:
				self.addResult(qr)


	def __doAddModel(self, model):
		"""Add the checked model to the payload."""
		pass
		

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


	# ============= Embedded: ModelWrap ===================

	class ModelData(object):
		"""Wraps a query result to include only outgoing data."""

		def __init__(self, model):
			self.appName = model.get_ontology_name()
			self.modName = None
			self.data = model.get_transportable()
			self.graph = None

			self.toRdf(model)

		def toRdf(self, model):
			# TODO: Temp test

			ns = Namespace(self.appName)
			ns_rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')

			graph = Graph()

			node = BNode()
			node = URIRef(model.url)
			graph.add((node, RDF.type, ns[model.get_rdf_class()]))

			#graph.add(sub, pred, obj)
			for k, v in self.data.iteritems():
				prd = ns[k]
				obj = Literal(v)
				graph.add((node, prd, obj))

			self.graph = graph.serialize()



