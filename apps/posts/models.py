from django.db import models
from sylph.core.endpoint.models import *
from markdown2 import markdown

class Post(ResourceTree):
	"""Post resources. Represent articles, posts, replies, etc."""

	# Title of the post. Required if a 'first' post.
	title = models.CharField(
				max_length=140, 
				blank=True, # XXX: Programatically, first posts can't be false
				null=False 
	)

	# The person who created the post. Can be null if anonymous or unknown.
	# TODO: Differentiate between 'anonymous' and 'unknown'. Or maybe not?
	# Maybe it should just be under the umbrella 'unknown'.
	created_by = models.ForeignKey('social.User', null=True)

	# Contents of the post
	contents = models.TextField(blank=True)

	# Markup type choices. 
	MARKUP_TYPE_CHOICES = (
		('P', 'Plaintext'),
		('M', 'Markdown'),
		#('W', 'Wiki markup'),
		('H', 'HTML (lite)'), # XXX: HTML must be filtered extensively. 
		('X', 'Unknown'),
	)
	markup_type = models.CharField(max_length=1, choices=MARKUP_TYPE_CHOICES, 
								   null=False, default='M')

	# Cannot send marked-up contents
	contents_markup_cache = models.TextField(blank=True)

	def get_absolute_url(self):
		return "/posts/view/%i/" % self.id

	def __unicode__(self):
		return self.title

	# A list of transportable RDF fields
	rdf_fields = [
			'title',
			'contents',
		]

	# ============= Content Markup ========================

	def contents_markdown(self):
		"""View a markdown-version of the contents."""
		if self.markup_type in ['P', 'X']:
			return self.contents

		if not self.contents_markup_cache:
			markup = markdown(self.contents) # TODO: More markup methods
			self.contents_markup_cache = markup
			self.save()

		return self.contents_markup_cache

	# ============= Model Meta ============================

	class Meta:
		"""Model metadata"""
		verbose_name = 'post'
		verbose_name_plural = 'posts'
		#order_with_respect_to = 'reply_to'
		#ordering

	# XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX
	# TODO: Use a model method to describe which fields cannot be transported
	# over RDF. (This is a bit hackish/primative, but it'll do.)
	# XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX 

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

	
