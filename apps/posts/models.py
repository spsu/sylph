

class Post(models.Model):
	"""Post resources. Represent articles, posts, replies, etc."""

	# XXX: Is-a or has-a resource?
	resource = models.OneToOneField('endpoint.Resource')

	reply_to = models.ForeignKey('self') # Can be null. 

	title = models.CharField(max_length=140)
	contents = models.TextField() # TODO: Plaintext? Markup?

	datetime_posted = models.DateTimeField()
	datetime_edited = models.DateTimeField()
	datetime_retrieved = models.DateTimeField()
	datetime_read = models.DateTimeField()

	access_uri = models.SlugField()


class Feed(models.Model):
	"""RSS/Atom feeds we bootstrap. 
	Don't require transformation rules."""
	# TODO: Should we combine Feeds and Sites? Make a sub-relation?

	uri_main = models.URLField(max_length=200)

	# Note: This is fetching the main feed. 
	# Represented in seconds. 
	fetch_every = PositiveIntegerField()

class Site(models.Model):
	"""Sites we bootstrap.
	Require HTML->XML transformation rules."""

	uri_main = models.URLField(max_length=200)

	rip_rules = '' # TODO: How to implement?
	rip_node = models.ForeignKey('endpoint.Node')

	# Note: This is fetching the main feed. 
	# Represented in seconds. 
	fetch_every = PositiveIntegerField()

	
# XXX XXX: Problem! Do we limit threads to 10,000 posts? What happens if a 
# spammer fills the thread up?
# Think about the networking, exchange, and spam deterrance.

	
