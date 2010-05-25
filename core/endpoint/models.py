from django.db import models
import datetime

"""
	'Endpoint Models' describe the data that is necessary for the protocol to
	function at all. These include some of the most fundamental datatypes in
	the system.
"""

# ============= Resource Manager ================
	
class ResourceManager(models.Manager):
	"""Custom manager for resources"""
	def get_by_natural_key(self, res_url):
		return self.get(url=res_url)

# ============ Resource =========================

class Resource(models.Model):
	"""
		The _Resource_ is the most fundamental datatype of the early and 
		prototypical Sylph architecture. It is absolutely key that we all agree
		on this and establish it as such. 

			>> Understanding the Resource is understanding Sylph. <<

		Resources in a sense represent 'network data files' that are uniquely
		identified by a URL and can be shared, updated, looked up at a cache if
		they go missing, etc. 

		Resources are built upon in an OO-hierarchy, adding the features 
		and fields required by the type of data we are modeling. 

		Currently, a model may be one of these types:

			* Resource -- A single "file" that doesn't reference other resources
						  unless it is built upon.

				* TreeResource -- A network "file" that can reference a root 
								  document as well as an immediate parent. Think
								  of post or email threads as being a use case
								  that would be well-represented here.


			> More resource-types will likely be added as need is found.

		Some of the data modeled in the system will NOT be a resource. Such an
		example is the 1:n email relation. Email addresses do not constitute 
		data that changes. They are immutable and will be replaced if changed,
		not 'edited'.

	"""

	objects = ResourceManager()

	# The URL corresponding to the resource. 
	# It is unique, and this can be enforced by ensuring only the producer can 
	# make a certain subset of URLs at their own domain / path. 
	url = models.URLField(max_length=200, unique=True)
	
	# Delete or refresh sementics.
	# XXX: Do I need a keep or expire flag?
	# Maybe the semantics of this flag can differ depending on type?
	# TODO: Can this be inferred from elsewhere in the system?
	stale = models.PositiveIntegerField(blank=True, default=0) 

	# Dates corresponding to the producer
	# XXX: Enforce date semantics in the code!
	datetime_created = models.DateTimeField(null=True, blank=True) 
	datetime_edited = models.DateTimeField(null=True, blank=True) 

	# Dates corresponding to the consumer
	# XXX: Consumer-only. Cannot send these!!
	# TODO: Strip any resource metadata being sent marked 'consumer-only'
	datetime_retrieved = models.DateTimeField(null=True, blank=True) 
	datetime_read = models.DateTimeField(null=True, blank=True) 

	# XXX: Is this proper?
	# A non-tranportable cache of reply count.
	# reply_count_cache = models.PositiveIntegerField(blank=True, default=0) 

	# A list of transportable RDF fields
	rdf_fields = [
			'url',
			'datetime_created',
			'datetime_edited'
		]

	def get_absolute_url(self):
		return "/resource/view/%i/" % self.id


	# ============= RDF Serilization Helpers ==============

	def get_transportable(self):
		"""Return the elements that can be transported over RDF payload."""
		dic = dict()
		fields = self.get_transportable_fields()

		for field in fields:
			if hasattr(self, field):
				dic[field] = getattr(self, field)

		return dic

	@classmethod
	def get_transportable_fields(cls):
		"""Return a list of the names of the fields that can be transported."""

		# TODO: Won't multiple-inheritance be an issue?
		if hasattr(cls.__bases__[0], 'rdf_fields'):
			fields = cls.__bases__[0].get_transportable_fields()
			for field in cls.rdf_fields:
				if field in fields:
					continue
				fields.append(field)
			return fields

		return cls.rdf_fields


	def get_ontology_name(self):
		"""Generates the ontology name (THIS ONLY FITS SHORT-TERM OBJECTIVE!)"""
		# TODO: Temp fix
		name = str(type(self))
		name = '/' + name[8:-2] + '#'
		return name.replace('.', '/').replace('/models/', '_')

	def get_rdf_class(self):
		return self.__class__.__name__


	# ============= Model Meta =====================
	
	class Meta:
		verbose_name = 'resource'
		verbose_name_plural = 'resources'


# ============ Resource List ====================

class ResourceList(Resource):
	"""A type of resource that is capable of building a list."""

	# The absolute root of the response tree
	reply_to = models.ForeignKey('self', 
								 related_name='resource_set_reply',
								 null=True, blank=True)


# ============ Resource Tree ====================

class ResourceTree(Resource):
	"""A type of resource that is capable of building a tree.

	Example, posts:

		* Rooted Post
			* Reply to root
			* Reply to root
				* Reply to non-root
	"""

	# The absolute root of the response tree
	reply_to_root = models.ForeignKey('self', 
									  related_name='resource_set_root',
									  null=True, blank=True)

	# The immediate parent of the response
	reply_to_parent = models.ForeignKey('self', 
										related_name='resource_set_parent',
										null=True, blank=True)

	# A list of transportable RDF fields
	rdf_fields = [
			'reply_to_root',
			'reply_to_parent',
		]

	# ============= RDF Serilization Helpers ==============

	def get_transportable(self):
		"""Return the elements that can be transported over RDF payload."""
		ret = super(ResourceTree, self).get_transportable()
		cur = {
			'reply_to_root': self.reply_to_root,
			'reply_to_parent': self.reply_to_parent,
		}
		for k in cur.keys():
			ret[k] = cur[k]

		return ret


# ============ Node =============================

# TODO: UserNodes and MachineNodes
# TODO: FollowerNodes and FollowingNodes
# TODO: Generic and Advanced permissions

class Node(models.Model):
	"""Describes the basic nodes in the first iteration of this software."""
	# XXX NOTE: A user has a node, not a node has a user!

	# Node access path
	url = models.URLField(max_length=200)
	
	# Name of the node
	name = models.CharField(max_length=40)

	# TODO: Media access suburl (is that even necessary?)
	#media_url = models.URLField(max_length=200)

	# TODO: The type of node.
	# Maybe just User Nodes and Machine/Utility Nodes, whereby utility nodes
	# will provide a certain number of services.  
	NODE_TYPES = (
		('X', 'Unknown'),
		('U', 'User Node'),
		('M', 'Machine Node'),
		#('C', 'Cache Node'), # Usually static files
		#('G', 'Group Node'),
		#('D', 'Directory Node'), # Look up people or resources
	)
	node_type = models.CharField(max_length=1, choices=NODE_TYPES)

	# First time nodes are added, they must be resolved. 
	is_to_resolve = models.BooleanField()

	datetime_added = models.DateTimeField()
	datetime_last_resolved = models.DateTimeField() # Includes "status pinging"

	# For events originating at the local node
	datetime_last_pushed_to = models.DateTimeField()
	datetime_last_pulled_from = models.DateTimeField()

	# For events originating at the remote node
	datetime_last_pulled_from_us = models.DateTimeField()
	datetime_last_pushed_to_us = models.DateTimeField()

	# The kinds of status a node can have
	STATUS_TYPES = (
		('U', 'Unknown'),
		('A', 'Available'),
		('E', 'Server Error'),
		('R', 'Unresolvable'),
    )
	status = models.CharField(max_length=1, choices=STATUS_TYPES)

	def get_absolute_url(self):
		return "/node/view/%i/" % self.id

	# XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX
	# TODO: Use a model method to describe which fields cannot be transported
	# over RDF. (This is a bit hackish/primative, but it'll do.)
	# XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX 


