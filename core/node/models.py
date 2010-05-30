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

	"""Node physical query endpoint. Required and Unique."""
	uri = models.URLField(max_length=200, unique=True, verify_exists=False)
	
	"""A short name for the node."""
	name = models.CharField(max_length=20, null=False, blank=True)

	"""A description for the node (as set by the node owner)."""
	description = models.CharField(max_length=255, null=False, blank=True)

	"""A personal description/note for the node."""
	own_description = models.CharField(max_length=255, null=False, blank=True)

	# TODO: Media access suburl (is that even necessary?)
	#media_url = models.URLField(max_length=200)

	# TODO: The type of node.
	# Maybe just User Nodes and Machine/Utility Nodes, whereby utility nodes
	# will provide a certain number of services.  
	NODE_TYPE_CHOICES = (
		('X', 'Unknown'),
		('U', 'User Node'),
		('M', 'Machine Node'),
		#('C', 'Cache Node'), # Usually static files
		#('G', 'Group Node'),
		#('D', 'Directory Node'), # Look up people or resources
	)
	node_type = models.CharField(max_length=1, choices=NODE_TYPE_CHOICES)

	"""First time nodes are added, they must be resolved.""" 
	is_yet_to_resolve = models.BooleanField()

	"""Date the node was first added to the server."""
	datetime_added = models.DateTimeField(default=datetime.today)

	"""Date the last communication with the node occurred on."""
	datetime_last_resolved = models.DateTimeField(null=True)

	"""For events originating at the local node"""
	datetime_last_pushed_to = models.DateTimeField(null=True)
	datetime_last_pulled_from = models.DateTimeField(null=True)

	"""For events originating at the remote node"""
	datetime_last_pulled_from_us = models.DateTimeField(null=True)
	datetime_last_pushed_to_us = models.DateTimeField(null=True)

	"""Date when node parameters were changed by the owner"""
	datetime_edited = models.DateTimeField(null=True)

	"""The types of status a node can have"""
	STATUS_TYPE_CHOICES = (
		('U', 'Unknown'),
		('A', 'Available'),
		('E', 'Server Error'),
		('R', 'Unresolvable'),
    )
	status = models.CharField(max_length=1, choices=STATUS_TYPE_CHOICES, 
							  null=False, blank=False, default='U')

	# ============= Django Methods and Metadata ===========
	
	class Meta:
		verbose_name = 'node'
		verbose_name_plural = 'nodes'

	def get_absolute_url(self):
		return "/node/view/%i/" % self.id

	def __unicode__(self):
		return self.uri

