# Sylph
from sylph.core.endpoint.models import Resource

# Django
from django.db.models.query import QuerySet

# RDF Lib
import rdflib
from rdflib.Graph import ConjunctiveGraph as Graph
from rdflib import Namespace, URIRef, Literal, BNode, RDF

# XXX XXX: See IntermediaryOld for removed code. 

class Intermediary(object):
	"""
	Just store some queried data. 
	"""

	def __init__(self):
		# TODO
		self.data = [] 


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



