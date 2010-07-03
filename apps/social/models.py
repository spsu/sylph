from django.db import models
from sylph.core.resource.models import Resource
#from sylph.core.resource.models import ResourceDigraphEdge
from sylph.apps.post.models import Post
from sylph.apps.user.models import User

class Knows(Resource):
	"""
	Knows represents a connection between two users, but is realized as
	a digraph instead of a forced, edgeless connection that must be
	maintained at both ends.

	This is in a way similar to foaf:knows and will be built as such.

	Usage:
		Knows(origin=personA, destination=personB, description='...')
	"""

	# TODO: Programatically enforce 'origin' and 'destination' to be users

	description = models.CharField(max_length=255, null=False, blank=True)

	origin = models.ForeignKey(User, related_name='set_origin', null=True, blank=True)
	destination = models.ForeignKey(User, related_name='set_destination', null=True, blank=True)

	class Meta(Resource.Meta):
		pass

class ProfilePost(Post):
	"""
	A profile post is similar to a Facebook 'wall post'.

	(I think those are kind of stupid, but whatever... they may be
	practical.)
	"""

	for_user = models.ForeignKey(User, related_name='for_user')

	class Meta(Post.Meta):
		pass

