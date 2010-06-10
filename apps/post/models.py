from django.db import models
from sylph.core.resource.models import ResourceTree
from sylph.utils.markdown2 import markdown

from datetime import datetime

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
	author = models.ForeignKey('social.User', null=True)

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
	contents_cache_datetime = models.DateTimeField(null=True, blank=True)

	# ============= Model-specific methods ================

	def contents_markdown(self):
		print "contents_markdown is deprecated" # XXX: DEPRECATED 
		return self.contents_with_markup()

	def contents_with_markup(self):
		"""Get the contents with markup."""
		if self.markup_type in ['P', 'X']: # TODO: Notify template of unsafety
			return self.contents

		stale = False
		if not self.contents_markup_cache or \
			(self.datetime_edited and \
				self.datetime_edited >= self.contents_cache_datetime):
					stale = True

		if stale:
			markup = markdown(self.contents) # TODO: More markup methods
			self.contents_markup_cache = markup
			self.contents_cache_datetime = datetime.today()
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

class PostCacheData(models.Model):
	"""
	NOT A RESOURCE

	In the case where we download posts by users not tracked by our
	system, we store some basic info on them here.
	"""
	post = models.ForeignKey('Post')

	"""Name stored with a post. Can be a username, first name, whatever."""
	name = models.CharField(max_length=60, blank=True, null=False)

	"""URI of the user resource in the event we want to look them up."""
	user_uri = models.CharField(max_length=255, blank=True, null=False)

	#"""URI of the user's node in the event we want to look them up."""
	#node_uri = models.CharField(max_length=255, blank=True, null=False)

	"""An optional website URI."""
	web_uri = models.CharField(max_length=255, blank=True, null=False)

	"""An optional email address."""
	email = models.CharField(max_length=60, blank=True, null=False)


class PostReferences(models.Model):
	"""
	NOT A RESOURCE

	Aggregate the links to other resources, either computationally via
	the assistance of a backend job, or delivered along with a payload,
	eg: <references>URI</references>.

	This allows fast querying and graph search (theoretically).\

	Nomenclature (work in progress):
		* A _link_ is an html/web anchor.
		* A _reference_ is a Sylph connection between resources.
	"""

	post = models.ForeignKey('Post', related_name='set_post')
	linked_resource = models.ForeignKey('resource.Resource')

	# TODO: dynamic = models.CharField() # explain the semantics of the linkage

