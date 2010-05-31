from django.db import models
from sylph.apps.post.models import Post
from sylph.core.resource.models import Resource

class BlogItem(Post):
	"""
	A BlogItem constitutes a blog entry. It is further specialized from 
	Post by allowing crafted pagination and (TODO) attached galleries.
	"""

	# ============= Sylph Metadata ========================

	rdf_fields = [
		'description',
		'is_multipage',
	]

	# ============= Model Fields ==========================

	"""
	An optional description of or excerpt from the contents of the 
	posting.
	"""
	description = models.CharField(max_length=255, blank=True, null=False)

	"""
	Whether the model spans multiple pages (as defined by the author
	in the markup of the text itself). A sophisticated Sylph client 
	should be able to override or autoset this clientside. 
	"""
	is_multipage = models.BooleanField(default=False)

	# TODO: Authors table (n:m)

	# TODO: Gallery table?


# TODO: Should BlogResponse be created?


