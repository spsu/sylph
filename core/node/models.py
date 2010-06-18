from django.db import models
from sylph.core.resource.models import Resource
from datetime import datetime
import os
import math
from base64 import b64encode

# ============ Nodes ======================================

# TODO: UserNodes and MachineNodes
# TODO: FollowerNodes and FollowingNodes
# TODO: Generic and Advanced permissions

class Node(Resource):
	"""
	Nodes are the machines on the web that can share and communicate
	resources with one another.

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
			'datetime_edited',
	]

	class_name = 'Node'

	# ============= Model Fields ==========================

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
	#datetime_added = models.DateTimeField(default=datetime.today)

	"""Date the last successful communication with the node occurred on."""
	datetime_last_resolved = models.DateTimeField(null=True)

	"""Date the last failed communication occurred."""
	datetime_last_failed = models.DateTimeField(null=True)

	"""Date when node parameters were changed by the owner"""
	#datetime_edited = models.DateTimeField(null=True)

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

	"""
	In the process of mutually adding nodes, we exchange secret keys.
	This isn't for security, but rather to avoid 'doorbell ditching'.
	These keys are uniquely generated for each Node pairing.
	Once PGP is in place, don't use this anymore.
	"""
	# XXX XXX XXX: This isn't based on actual cryptography...
	doorbell_key_ours = models.CharField(max_length=100)
	doorbell_key_theirs = model.CharField(max_length=100)

	DOORBELL_STATUS_CHOICES = (
		('0', 'Ungenerated'),
		# One party has generated a key
		('1', 'One key generated.'),
		# Both parties have generated a key
		('2', 'Both keys generated.'),
		# Both parties have generated a key, and the first party confirmed.
		('3', 'Both keys confirmed!'),
    )
	doorbell_status = models.CharField(max_length=1,
								choices=DOORBELL_STATUS_CHOICES,
								null=False, blank=False, default='0')

	# ============= Node-specific functionality ===========

	def generate_key(self, replace=False):
		"""Generate our 'doorbell key' for the other node.
		NOTE: DOES NOT SAVE!"""
		if self.doorbell_key_ours and not replace:
				return
		self.doorbell_key_ours = b64encode(os.urandom(100)[:-2]
		return

	def check_keys(self, our_key, their_key):
		pass

	# ============= RDF Serilization Helpers ==============

	def get_ontology_name(self):
		"""Heuristic to generate the ontology name."""
		# TODO: Temp fix, and does it actually work??
		name = str(type(self))
		name = '/' + name[8:-2] + '#'
		return name.replace('.', '/').replace('/models/', '_')

	def get_rdf_class(self):
		return self.__class__.__name__


	# ============= Template Helpers ======================

	def is_ours(self):
		"""Returns whether this node is ours."""
		return self.id == 2

	def is_not_ours(self):
		"""Returns whether this node is not ours."""
		return self.id != 2

	def status_color(self):
		"""Return a status color for visualization. Temporary."""
		if self.id == 2:
			return 'white'
		if self.is_yet_to_resolve:
			return 'red'
		if self.status == 'AVAIL':
			return 'green'
		return 'red'

	def get_status(self):
		if self.id == 2:
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
		return "node: " + self.uri

