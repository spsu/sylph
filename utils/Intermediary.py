# Django
from django.conf import settings
from django.db import models
from django.db.models.query import QuerySet

# RdfLib
from rdflib.Graph import ConjunctiveGraph as Graph
from rdflib import URIRef, Literal, BNode, RDF
from rdflib import Namespace as NS

# Sylph
from sylph.core.resource.models import Resource, ResourceTree
from sylph.core.node.models import Node

from types import NoneType

class Intermediary(object):
	"""
	Intermediary transforms QueryResults and singular model instances
	from Django's ORM into RDF payloads to send over the wire. This is
	how we will accomplish communication in Sylph.
	"""

	# ============= Namespaces ============================

	"""The Sylph Namespace as well as other popular RDF namespaces."""
	NAMESPACES = {
		# Namespace for the Sylph Protocol & Models
		# TODO: These aren't actual URIs
		# TODO: Models need ontologies to go with them!
		'sylph': NS('http://digitalsubstance.com/sylph/0.1/ns#'),
		'model': NS('http://digitalsubstance.com/model/0.1/ns#'),

		# Other popular ontologies -- consider using/interoperating with them!
		'rdf': NS('http://www.w3.org/1999/02/22-rdf-syntax-ns#'),
		'rdfs': NS('http://www.w3.org/2000/01/rdf-schema#'),
		'owl': NS('http://www.w3.org/2002/07/owl#'),
		'xmls': NS('http://www.w3.org/2001/XMLSchema#'),
		'dc': NS('http://purl.org/dc/elements/1.1/'),
		'dcterms': NS('http://purl.org/dc/terms/'),
		'foaf': NS('http://xmlns.com/foaf/0.1/'),
	}

	# ============= CTOR ==================================

	def __init__(self, obj=None):
		"""Intermediary constructor. May take an optional first result
		to add to the graph."""

		"""Subgraphs are held for every model/queryresult added."""
		self.subgraphs = []

		if obj:
			self.add(obj)


	# ============= Add ===================================

	def add(self, obj):
		"""Add a query result or model into the intermediary."""
		if type(obj) not in [list, tuple, QuerySet]:
			if not isinstance(obj, Resource) and \
			   not isinstance(obj, Node):
					raise TypeError, \
						  "Query Result must be a Resource or Node!\n"

			#mod = self.ModelData(obj)
			#self.data.append(mod)
			self.__convert_to_triples(obj)
			return 

		# Recurse over list
		if type(obj) in [list, tuple, QuerySet]:
			for o in obj:
				self.add(o)


	def __convert_to_triples(self, model):
		"""Converts each model/query result into its own graph to be 
		merged the graph returned by to_rdf()."""
		sylph = self.NAMESPACES['sylph']

		graph = Graph()
		graphNum = len(self.subgraphs)

		node = URIRef(model.uri) # The Resource
		graph.add((node, RDF.type, sylph[model.get_rdf_class()])) # Datatype

		data = model.get_transportable()

		# Performs graph.add(sub, pred, obj)
		for k, v in data.iteritems():
			obj = None
			if k == 'uri':
				continue # already done

			# Blank values transported because we may be 'erasing' them
			if not v:
				if type(v) in [str, unicode]:
					obj = Literal('')
				if type(v) is NoneType:
					obj = sylph['None']

			if isinstance(v, (models.Model, Resource, ResourceTree)):
				# TODO/XXX: This is slow as hell. Hits the database every 
				# single time this codepath is reached. 
				# For now, forget performance. Work on this later...
				obj = URIRef(v.uri) 

			if not obj:
				obj = Literal(v) # Handles int, float, etc.

			graph.add((node, sylph[k], obj))

		self.subgraphs.append(graph)


	def to_rdf(self, format='settings'):
		"""Convert the intermediary store into RDF."""
		graph = Graph()
		for k, v in self.NAMESPACES.iteritems():
			graph.bind(k, v)

		for g in self.subgraphs:
			graph += g

		if format == 'settings':
			format = settings.RDF_SERIALIZATION

		return graph.serialize(format=format)

