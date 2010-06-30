from django.db import models
from sylph.apps.post.models import Post
from sylph.core.resource.models import Resource

# XXX XXX XXX IDEA: comments are a *separate app* entirely!

# ============ BlogItem =========================

class BlogItem(Post):
	"""
	Resource > ResourceTree > Post > BlogItem

	A BlogItem constitutes a blog entry. It is further specialized from
	Post by allowing crafted pagination and (TODO) attached galleries.

	Important fields reference: # TEMPORARY NOTE TO SELF!
	-----------------------------------------------------

						   :: Resource ::
		* uri
		* datetime_created
		* datetime_edited

					     :: ResourceTree ::

		Maybe in rare events a blog post can be a response to another:
			* reply_to_root = NULL (usually) or BlogItem
			* reply_to_parent = NULL (usually) or BlogItem

						    :: Post ::

		* title
		* author - FK - UNLESS THIS IS A __BootstrapBlogItem__
		* contents
		* contents_markup_type
		* license = {CC (multiple), PubDomain, Copyright, Unknown(AssumeCopy)}

						  :: BlogItem ::

		* summary [+generated_excerpt]
		* is_multipage (pagenation is in contents. Post needs to ignore!)
		+ Far more advanced presentation methods. Focus on readability.

					  :: BootstrapBlogItem::

		* site - FK (can be null)
		* www_author_name, www_author_website, www_author_email

	"""

	# ============= Sylph Metadata ========================

	rdf_fields = [
		'summary',
		'is_multipage',
	]

	rdf_ignore = [
		'generated_excerpt',
	]

	# ============= Model Fields ==========================

	"""
	An optional description of or excerpt from the contents of the
	posting.
	"""
	summary = models.CharField(max_length=255, blank=True, null=False)

	"""
	An optional excerpt from the contents that has been algorithmically
	selected by *our* software.
	"""
	generated_excerpt = models.CharField(max_length=255, blank=True,
											null=False)

	"""
	Whether the model spans multiple pages (as defined by the author
	in the markup of the text itself). A sophisticated Sylph client
	should be able to override or autoset this clientside.
	"""
	is_multipage = models.BooleanField(default=False)

	# TODO: Authors table (n:m)

	# TODO: Gallery table?

	def get_description(self):
		"""Return either the human-defined description or a generated
		excerpt. If there is no excerpt, generate one and cache it."""
		if self.description:
			return self.description
		if self.generated_excerpt:
			return self.generated_excerpt
		# TODO: Generate excerpt and save
		return None

	def contents_or_summary(self):
		"""REturn the content or the summary."""
		if self.contents:
			return self.contents
		if self.summary:
			return "(Summary) " + self.summary

# ============ BootstrapBlogItem ==========================

# XXX: Do a monolithic app with both bootstrap and distributed (for now)

class BootstrapBlogItem(BlogItem):
	"""
	Resouce > ResourceTree > Post > BlogItem > BootstrapBlogItem

	A BlogItem that is retrieved from a 'dumb' www website (with no
	semantic cabability).

		* uri = webpage where obtained (best if original loc.)
		* author = null (usually)
		* datetime_created = date
		* datetime_edited = edit date (rarely available)
	"""

	# ============= Sylph Metadata ========================

	rdf_fields = [
		#'site',
	]

	# ============= Model Fields ==========================

	#site = models.ForeignKey('Site')

	"""Author string. Useful to keep in the event the author isn't yet
	in the distributed web. (Of course, we may get that info somehow.)
	"""
	www_author_name = models.CharField(max_length=60, blank=True, null=False)

	"""Contact methods for the author."""
	www_author_website = models.CharField(max_length=255, blank=True, null=False)
	www_author_email = models.CharField(max_length=60, blank=True, null=False)


