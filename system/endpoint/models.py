from django.db import models

# Endpoint-oriented models. 

class Resource(models.Model):
	url = models.URLField(max_length=200)
	
	# XXX: Do I need a keep or expire flag?
	# Maybe the semantics of this flag can differ depending on type?

	stale = models.PositiveIntegerField() # Delete or refresh sementics.

class Node(models.Model):
	# Node access path
	endpoint_url = models.URLField(max_length=200)
	media_url = models.URLField(max_length=200)

	# XXX: A user has a node, not a node has a user!

	# The type of node. 
	NODE_TYPES = (
		('U', 'User Node'),
		('C', 'Cache Node'), # Usually static files
		('G', 'Group Node'),
    )
    node_type = models.CharField(max_length=1, choices=NODE_TYPES)

	# First time nodes are added, they must be resolved. 
	is_to_resolve = models.BooleanField()

	datetime_added = models.DateTimeField()
	datetime_last_resolved = models.DateTimeField()

	# The kinds of status a node can have
	STATUS_TYPES = (
		('A', 'Available'),
		('E', 'Server Error'),
		('U', 'Unresolvable'),
    )
	status = = models.CharField(max_length=1, choices=STATUS_TYPES)

class FollowingNodes(models.Model):
	"""The nodes that we are following."""
	pass

class FollowerNodes(models.Model):
	"""The nodes that are following us."""

class FollowingNodePermissions(models.Model):
	"""Permissions we were granted for the nodes we are following."""

class FollowerNodePermissions(models.Model):
	"""Permissions we have granted to follower nodes."""

	node = models.ForeignKey('Node')

# XXX: There's a lot more complexity in permissions than I think there is
#		I need to carefully analyze this, perrhaps develop this after the
#		first networking iteration. 


