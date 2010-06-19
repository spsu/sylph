from django.db import models
from sylph.core.resource.models import Resource, ResourceDigraphEdge
from sylph.apps.post.models import Post

class Knows(ResourceDigraphEdge):
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


class ProfilePost(Post):
	"""
	A profile post is similar to a Facebook 'wall post'.

	(I think those are kind of stupid, but whatever... they may be
	practical.)
	"""

	for_user = models.ForeignKey('user.User')


