from django.db import models
from sylph.core.endpoint.models import Resource

class Post(models.Model):
#class Post(Resource):
	"""Post resources. Represent articles, posts, replies, etc."""

	# XXX: Is-a or has-a resource?
	#resource = models.OneToOneField('endpoint.Resource')

	#reply_to = models.ForeignKey('self') # Can be null. 

	title = models.CharField(
				max_length=140, 
				blank=True, # Programatically, first posts can't be false
				null=False 
	)

	contents = models.TextField(
				blank=True)

	# XXX: Doesn't matter yet...
	#contents_markup = models.TextField(
	#			blank=True)

	# XXX: ALL ARE TEMP NULL/BLANK
	datetime_posted = models.DateTimeField(null=True, blank=True) 
	datetime_edited = models.DateTimeField(null=True, blank=True) 
	datetime_retrieved = models.DateTimeField(null=True, blank=True) 
	datetime_read = models.DateTimeField(null=True, blank=True) 

	#access_uri = models.SlugField()

	def __unicode__(self):
		return self.title



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

	
# XXX XXX: Problem! Do we limit threads to 10,000 posts? What happens if a 
# spammer fills the thread up?
# Think about the networking, exchange, and spam deterrance.

	
