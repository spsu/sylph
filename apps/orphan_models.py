

#==============================================================================

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

