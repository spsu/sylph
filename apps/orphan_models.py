# ==================== core.endpoint.models ====================================

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





#===============================================================================

# XXX/TODO: This is a list of orphaned models. 


class Feed(models.Model):
	"""RSS/Atom feeds we bootstrap. 
	Don't require transformation rules."""
	# TODO: Should we combine Feeds and Sites? Make a sub-relation?

	uri_main = models.URLField(max_length=200)

	# Note: This is fetching the main feed. 
	# Represented in seconds. 
	fetch_every = models.PositiveIntegerField()

class Site(models.Model):
	"""Sites we bootstrap.
	Require HTML->XML transformation rules."""

	uri_main = models.URLField(max_length=200)

	rip_rules = '' # TODO: How to implement?
	rip_node = models.ForeignKey('endpoint.Node')

	# Note: This is fetching the main feed. 
	# Represented in seconds. 
	fetch_every = models.PositiveIntegerField()

	
# TODO/XXX: Problem! Do we limit threads to 10,000 posts? What happens if a 
# spammer fills the thread up?
# Think about the networking, exchange, and spam deterrance.

