from django.db import models

# Endpoint-oriented models. 

class Resource(models.Model):
	url = models.URLField(max_length=200)
	
	# XXX: Do I need a keep or expire flag?
	# Maybe the semantics of this flag can differ depending on type?

	stale = models.PositiveIntegerField() # Delete or refresh sementics.

	# Resource can be response to other resource.
	# Usually NULL. 
	reply_to = models.ForeignKey('self')

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



