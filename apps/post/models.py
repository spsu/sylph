from django.db import models
from sylph.core.endpoint.models import ResourceTree
from markdown2 import markdown

class Post(ResourceTree):
	"""
	Posts represent any content with a title and a main body of text.

	As Post decends from ResourceTree, posts have the capability to 
	have both an absolute root parent as well as an immediate parent.

	The Post model is further extended in other applications. Commonly 
	it is used to represent blog items, articles, threaded comments, 
	etc.
	"""

	# ============= Sylph Metadata ========================

	# A list of transportable RDF fields
	rdf_fields = [
			'title',
			'contents',
	]

	# ============= Model Fields ==========================

	# Title of the post. Required if a 'first' post.
	title = models.CharField(
				max_length=100, 
				blank=True, # XXX: Programatically enforced for first posts.
				null=False 
	)

	# The person who created the post. Can be null if anonymous or unknown.
	# TODO: Differentiate between 'anonymous' and 'unknown'. Or maybe not?
	# Maybe both should fall under the umbrella term 'unknown'.
	#created_by = models.ForeignKey('social.User', null=True)

	# Contents of the post
	contents = models.TextField(blank=True)

	# How the content is marked up. 
	MARKUP_TYPE_CHOICES = (
		('P', 'Plaintext'),
		('M', 'Markdown'),
		('H', 'HTML (lite)'), # XXX: HTML must be filtered extensively. 
		('X', 'Unknown'),
	)
	markup_type = models.CharField(max_length=1, choices=MARKUP_TYPE_CHOICES, 
								   null=False, default='M')

	# Cannot send marked-up contents
	contents_markup_cache = models.TextField(blank=True)

	# ============= Model-specific methods ================

	def contents_markdown(self):
		"""View a markdown-version of the contents."""
		if self.markup_type in ['P', 'X']:
			return self.contents

		if not self.contents_markup_cache:
			markup = markdown(self.contents) # TODO: More markup methods
			self.contents_markup_cache = markup
			self.save()

		return self.contents_markup_cache

	# ============= Django Methods and Metadata ===========

	class Meta:
		verbose_name = 'post'
		verbose_name_plural = 'posts'
		#ordering = ['-datetime_created']

	def get_absolute_url(self):
		return "/post/view/%i/" % self.id

	def __unicode__(self):
		return self.title

