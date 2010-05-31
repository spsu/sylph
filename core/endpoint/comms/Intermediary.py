# Sylph
from sylph.core.resource.models import Resource, ResourceTree

# Django
from django.db import models
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

		# Each result set as it is added
		self.resultSets = []

		# Individual records
		self.records = [] 

		# Resource FKs that need urls
		self.needUrls = []

		# Output graph
		self.graph = None
		self.subgraphs = []


	# ============= Add Result ============================

	def addResult(self, queryRet):
		"""Add a query result to the intermediary."""
		if type(queryRet) not in [list, tuple, QuerySet]:
			if not isinstance(queryRet, Resource):
				raise TypeError, "Query Result must be a Resource!\n"

			#mod = self.ModelData(queryRet)
			#self.data.append(mod)
			self.__addTriples(queryRet)
			return 

		if type(queryRet) in [list, tuple, QuerySet]:
			for qr in queryRet:
				self.addResult(qr)


	def __addTriples(self, model):
		# TODO TEST
		
		ns = Namespace(model.get_ontology_name())
		ns_rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')

		data = model.get_transportable()

		graph = Graph()
		graphNum = len(self.subgraphs)

		node = URIRef(model.url) # The Resource
		graph.add((node, RDF.type, ns[model.get_rdf_class()])) # RDF Datatype

		needUrls = []

		#graph.add(sub, pred, obj)
		classes = (models.Model, Resource, ResourceTree)
		for k, v in data.iteritems():
			obj = None

			if k == 'url':
				continue # already done

			if not v:
				continue # TODO: This shouldn't always be the case!

			if isinstance(v, classes):
				# FIXME: This is slow as hell. Hits the database every single 
				# time this codepath is reached. 
				# XXX: For now, forget performance. Work on this later...
				#self.needUrls.append((graphNum, k, v)) 
				#continue
				obj = URIRef(v.url) 

			if not obj:
				obj = Literal(v)

			prd = ns[k]
			graph.add((node, prd, obj))

		self.subgraphs.append(graph)

	def __addNamespace(self, namespace):
		pass
		

	def __getNeededUrls(self): # XXX: For now, forget performance. 
		urls = []
		for graphNum, k, v in self.needUrls:
			print k
			print v.url


		#for self.needUrls:

		#objs = Resource.objects.get(pk__in = urls).only("url")


	def toRdf(self):
		self.graph = Graph()
		ns = Namespace('/sylph/apps/posts_Post#')
		self.graph.bind('sylphPost', ns)

		for graph in self.subgraphs:
			self.graph += graph

		#self.__getNeededUrls() # XXX: For now, forget performance. 

		return self.graph.serialize(format='n3')



