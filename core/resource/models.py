from django.db import models
from django.db.models import signals
from django.dispatch import dispatcher

import datetime
import re

"""
Resources are the fundamental datatype of the system.
TODO: Documentation.
"""

# TODO: Consider 'ResourceRef' with just uri and make 'Resource' a decendant
# This will be for the purpose of referencing resources and having no data
# associated with them.

# ============ Resource ===================================

class Resource(models.Model):
	"""
	The _Resource_ is the most fundamental datatype of the early and
	prototypical Sylph architecture.

		>> Understanding the Resource is understanding Sylph. <<

	Resources in a sense represent 'network data files' that are
	uniquely identified by a URL and can be shared, updated, looked up
	at a cache if they go missing, etc. etc.

	Resources are built upon in an OO-hierarchy, adding the features
	and fields required by the type of data we are modeling.

	Currently, a model may be one of these types:

		* Resource -- A single "file" that doesn't reference other
					  resources unless it is subclassed.

			* ResourceTree -- A linked "file" that can reference a
							  root document as well as an immediate
							  parent. Think of post or email threads as
							  being a use case that would be well-
							  represented here.

			* ResourceDigraphEdge -- An edge in a digraph relationship.
									 It points to the origin and
									 destination Resources and can be
									 subclassed as necessary.

		> More resource-types will likely be added as need is found.

	Some of the data modeled in the system will NOT be a resource. Such
	an example is the 1:n email relation. Email addresses do not
	constitute data that changes. They are immutable and will be
	replaced if changed, not 'edited'.
	"""

	# ============= Sylph Metadata ========================

	"""A list of transportable RDF fields."""
	rdf_fields = [
		'uri',
		'datetime_created',
		'datetime_edited',
	]

	"""A list of fields *not* to transport."""
	rdf_ignore = [
		'datetime_added',
		'datetime_retrieved',
		'datetime_last_accessed',
	]

	class_name = 'endpoint.Resource'

	# ============= Model Fields ==========================

	"""
	The URI corresponding to the resource.
	It is unique, and this can be enforced by ensuring only the
	producer can make a certain subset of URIs at their own domain or
	path.
	"""
	uri = models.URLField(max_length=255, unique=True, verify_exists=False,
							blank=False, null=False)

	"""
	Describes the ultimate datatype of the resource. In OO
	perspectives, this is the most child type.
	"""
	#resource_type = models.ForeignKey('ResourceType')
	resource_type = models.CharField(max_length=30, null=False, blank=False,
										default='TODO') # TODO
	# Delete or refresh sementics.
	# TODO: Do I need a keep or expire flag?
	# Maybe the semantics of this flag can differ depending on type?
	# TODO: Can this be inferred from elsewhere in the system?
	stale = models.PositiveIntegerField(blank=True, default=0)

	"""
	Dates corresponding to the producer creating/editing the
	resource.
	"""
	# TODO/XXX: Enforce date semantics in the code!
	datetime_created = models.DateTimeField(null=True, blank=True)
	datetime_edited = models.DateTimeField(null=True, blank=True)

	"""
	Dates corresponding to the consumer using the resource.
	Do not send these to others!
	"""
	# TODO/XXX: Consumer-only. Cannot send these!!
	# TODO: Strip any resource metadata being sent marked 'consumer-only'
	datetime_added = models.DateTimeField(null=True, blank=True)
	datetime_retrieved = models.DateTimeField(null=True, blank=True) # XXX What??
	datetime_last_accessed = models.DateTimeField(null=True, blank=True) # XXX

	# TODO: Is this proper? (Should the type itself be responsible?)
	# A non-tranportable cache of reply count.
	# reply_count_cache = models.PositiveIntegerField(blank=True, default=0)

	# ============= RDF Serilization Helpers ==============

	def get_transportable(self):
		"""Return all data that can be transported over RDF payload."""
		dic = dict()
		fields = self.get_transportable_fields()

		for field in fields:
			if hasattr(self, field):
				dic[field] = getattr(self, field)

		return dic

	@classmethod
	def get_transportable_fields(cls):
		"""
		Return a list of the names of the fields that can be
		transported, minus the fields that cannot be transported.
		"""

		def get_transportable(cls):
			"""Recursively builds a list of the fields that CAN
			be transported over RDF given the model rules."""
			# TODO: Multiple-inheritance issue
			if not hasattr(cls.__bases__[0], 'rdf_fields'):
				return cls.rdf_fields
			else:
				fields = get_transportable(cls.__bases__[0])
				for field in cls.rdf_fields:
					if field in fields:
						continue
					fields.append(field)
				return fields

		def get_ignorable(cls):
			"""Recursively builds a list of the fields that CANNOT
			be transported over RDF given the model rules."""
			# TODO: Multiple-inheritance issue
			if not hasattr(cls.__bases__[0], 'rdf_ignore'):
				return cls.rdf_ignore
			else:
				fields = get_ignorable(cls.__bases__[0])
				for field in cls.rdf_ignore:
					if field in fields:
						continue
					fields.append(field)
				return fields

		# Build the list
		fields = get_transportable(cls)
		ignorable = get_ignorable(cls)
		for v in ignorable:
			if v in fields:
				fields.remove(v)

		return fields

	def get_ontology_name(self):
		"""Generates the ontology name (THIS ONLY FITS SHORT-TERM OBJECTIVE!)"""
		# TODO: Temp fix
		name = str(type(self))
		name = '/' + name[8:-2] + '#'
		return name.replace('.', '/').replace('/models/', '_')

	def get_rdf_class(self):
		return self.__class__.__name__

	# ============= Django Methods and Metadata ===========

	class Meta:
		abstract = True
		verbose_name = 'resource'
		verbose_name_plural = 'resources'

	def get_absolute_url(self):
		return "/resource/view/%i/" % self.pk

	def wrap_uri(self, length=45):
		ret = ''
		ln = 0
		while ln*length < len(self.uri):
			ret += self.uri[ln*length:(ln+1)*length] + "\n"
			ln += 1

		return ret[0:-1]

	def __unicode__(self):
		return self.uri


# ============ Resource Tree ==============================

class ResourceTree(Resource):
	"""
	ResourceTree is a Resource with links to up to two other Resources
	(of any type). An immediate "parent" of the ResourceTree object,
	and the absolute "root" of the tree.

	This double-linked capability allows us to potentially build tree
	structures that can be queried relatively quickly on the "root" and
	rebuilt in memory by the application via the "parents".

	An example is the posts.Post model, which is a direct decendant of
	ResourceTree and uses this feature:

		* Root Post
			* Reply to root
			* Reply to root
				* Reply to non-root

	Many of our datatypes will inherit from ResourceTree, although the
	use of both links is not necessary.
	"""

	# ============= Sylph Metadata ========================

	"""A list of transportable RDF fields."""
	rdf_fields = [
		'reply_to_root',
		'reply_to_parent',
	]

	"""A list of fields *not* to transport."""
	rdf_ignore = []

	class_name = 'endpoint.ResourceTree'

	# ============= Model Fields ==========================

	# The absolute root of the response tree
	reply_to_root = models.ForeignKey('self',
										related_name='resource_set_root',
										null=True, blank=True)

	# The immediate parent of the response
	reply_to_parent = models.ForeignKey('self',
										related_name='resource_set_parent',
										null=True, blank=True)

	class Meta(Resource.Meta):
		abstract = True

# ============ Resource Digraph Edge ======================

#class ResourceDigraphEdge(Resource):
#	"""
#	ResourceDigraphEdge is a representation of a directed graph edge
#	that is itself a resource. It has an origin and a destination
#	resource.
#
#	An example is the social.Knows model, which is a direct decendant
#	of ResourceDigraphEdge.
#	"""
#
#	# ============= Sylph Metadata ========================
#
#	"""A list of transportable RDF fields."""
#	rdf_fields = [
#			'origin',
#			'destination',
#	]
#
#	"""A list of fields *not* to transport."""
#	rdf_ignore = []
#
#	class_name = 'endpoint.ResourceDigraphEdge'
#
#	# ============= Model Fields ==========================
#
#	# The origin resource
#	origin = models.ForeignKey('Resource',
#								related_name='resource_set_origin',
#								null=False, blank=False)
#
#	# The destination resource
#	destination = models.ForeignKey('Resource',
#									related_name='resource_set_destination',
#									null=True, blank=True)
#
#
#	class Meta(Resource.Meta):
#		abstract = True

# ============ ResourceTypes ==============================

class ResourceType(models.Model):
	"""Represents the resource types installed in the system."""

	"""The unique key for each resource type."""
	key = models.CharField(unique=True, max_length=60, blank=False, null=False)

	"""A description of the resource type."""
	description = models.CharField(max_length=255, blank=True, null=False)

# ============ Model Managers =============================

# XXX: Causes exception: 'NoneType' object has no attribute '_meta'

#class ResourceManager(models.Manager):
#	"""Custom manager for resources"""
#	def get_by_natural_key(self, res_uri):
#		return self.get(uri=res_uri)

#Resource.objects = ResourceManager()

# ============ Signals ====================================

#def register_type(ModelType):
#	"""Register the type of each created resource.
#	This must be called in the models.py for each model type."""
#	import signals as sig_ # To avoid circular imports
#	signals.pre_save.connect(sig_.auto_apply_resource_type,
#								sender=ModelType)
#
#register_type(Resource)
#register_type(ResourceTree)
#register_type(ResourceDigraphEdge)

