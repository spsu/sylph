from rdflib.Graph import ConjunctiveGraph as Graph
from rdflib import URIRef, Literal, BNode, RDF
from rdflib import Namespace as NS

from sylph.utils.Intermediary import Intermediary

from cStringIO import StringIO

class RdfParser(object):
	def __init__(self, rdf):
		"""Init the parser with the graph string."""
		self.graph = Graph()
		self.graph.load(StringIO(rdf), format="n3")

	def extract(self, datatype):
		"""Extract all of the data of a given datatype."""
		data = []
		ns = Intermediary.NAMESPACES['sylph'] # TODO: Awkward.
		for sub in self.graph.subjects(RDF.type, ns[datatype]):
			idx = str(sub)
			item = {'uri': idx}
			for pred, obj in self.graph.predicate_objects(sub):
				if pred == RDF.type:
					continue
				if obj == ns['None']:
					obj = None
				if type(obj) == Literal:
					obj = str(obj)
				predstr = str(pred).rpartition('#')[2].rpartition('/')[2]
				item[predstr] = obj
			data.append(item)
		return data

