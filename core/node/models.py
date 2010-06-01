from django.db import models

from datetime import datetime

# ============ Nodes ======================================

# TODO: UserNodes and MachineNodes
# TODO: FollowerNodes and FollowingNodes
# TODO: Generic and Advanced permissions

class Node(models.Model): # NOT A RESOURCE!
	"""
	Nodes are the machines on the web that can share and communicate
	resources with one another. They are immutable and thus not 
	Resources themselves (as the data model exists thus far). 

	There can be user-owned Nodes, cache Nodes, directory Nodes, and
	so forth.

	Endpoint would probably be a better name for this, but I'll go with
	Node since the graph nature is more visible. 

	This is only a first-iteration model.
	"""

	# XXX NOTE: A user has a node, not a node has a user!

	# ============= Sylph Metadata ========================

	# A list of transportable RDF fields
	rdf_fields = [
			'uri',
			'name',
			'description', # TODO: own_description?
			'node_type',
			'protocol_version',
			'software_name',
			'software_version',
			'datetime_last_edited',
	]

	class_name = 'Node'

	# ============= Model Fields ==========================

	"""Node physical query endpoint. Required and Unique."""
	uri = models.URLField(max_length=200, unique=True, verify_exists=False)
	
	"""A short name for the node."""
	name = models.CharField(max_length=20, null=False, blank=True)

	"""A description for the node (as set by the node owner)."""
	description = models.CharField(max_length=255, null=False, blank=True)

	"""A personal description/note for the node. Never transport this!"""
	own_description = models.CharField(max_length=255, null=False, blank=True)

	# TODO: Media access suburl (is that even necessary?)
	#media_url = models.URLField(max_length=200)

	# TODO: The type of node.
	# Maybe just User Nodes and Machine/Utility Nodes, whereby utility nodes
	# will provide a certain number of services.  
	NODE_TYPE_CHOICES = (
		('X', 'Unknown'),
		('U', 'User Node'),
		('C', 'Cache Node'), # Usually static files
		('D', 'Directory Node'), # Look up people or resources
		#('G', 'Group Node'), # TODO: More types... eg. software repository		
	)
	node_type = models.CharField(max_length=1, choices=NODE_TYPE_CHOICES)

	"""Sylph Protocol version"""
	protocol_version = models.CharField(max_length=15, null=False, blank=True)

	"""Client Software name"""
	software_name = models.CharField(max_length=20, null=False, blank=True)

	"""Client Software version"""
	software_version = models.CharField(max_length=15, null=False, blank=True)

	"""First time nodes are added, they must be resolved.""" 
	is_yet_to_resolve = models.BooleanField()

	"""Date the node was first added to the server."""
	datetime_added = models.DateTimeField(default=datetime.today)

	"""Date the last successful communication with the node occurred on."""
	datetime_last_resolved = models.DateTimeField(null=True)

	"""Date the last failed communication occurred."""
	datetime_last_failed = models.DateTimeField(null=True)

	"""Date when node parameters were changed by the owner"""
	datetime_edited = models.DateTimeField(null=True)

	"""For events originating at the local node"""
	datetime_last_pushed_to = models.DateTimeField(null=True)
	datetime_last_pulled_from = models.DateTimeField(null=True)

	"""For events originating at the remote node"""
	datetime_last_pulled_from_us = models.DateTimeField(null=True)
	datetime_last_pushed_to_us = models.DateTimeField(null=True)

	"""The types of status a node can have"""
	STATUS_TYPE_CHOICES = (
		('U', 'Unknown status'),
		('HOST', 'Host does not resolve.'),
		('SERR', 'Server error.'),
		('EERR', 'Endpoint software error.'),
		('FLOOD', 'Server flooded / bandwidth issue.'),
		('ENDP', 'Not a valid endpoint.'),
		('AVAIL', 'Available / OK.'),
    )
	status = models.CharField(max_length=5, choices=STATUS_TYPE_CHOICES, 
							  null=False, blank=False, default='U')


	# ============= RDF Serilization Helpers ==============

	def get_transportable(self):
		"""
		Return the elements that can be transported over RDF payload.
		"""
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
		transported.
		"""
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
		"""Heuristic to generate the ontology name."""
		# TODO: Temp fix, and does it actually work??
		name = str(type(self))
		name = '/' + name[8:-2] + '#'
		return name.replace('.', '/').replace('/models/', '_')

	def get_rdf_class(self):
		return self.__class__.__name__


	# ============= Template Helpers ======================

	def status_color(self):
		"""Return a status color for visualization. Temporary."""
		if self.id == 1:
			return 'white'
		if self.is_yet_to_resolve:
			return 'red'
		if self.status == 'AVAIL':
			return 'green'
		return 'red'

	def get_status(self):
		if self.id == 1:
			return 'Our node'
		if self.is_yet_to_resolve:
			return 'Unresolved'
		if self.status == 'AVAIL':
			return "Good"
		return "Bad Status"

	# ============= Django Methods and Metadata ===========
	
	class Meta:
		verbose_name = 'node'
		verbose_name_plural = 'nodes'

	def get_absolute_url(self):
		return "/node/view/%i/" % self.id

	def protocol_compatibility(self, proto_version):
		"""Compare the protocol version with a compatibility checklist."""
		# TODO: allow lookup against a compatibility checklist
		return proto_version == self.protocol_version

	def __unicode__(self):
		return self.uri

