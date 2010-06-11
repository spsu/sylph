from django.db import model
from sylph.core.resource.models import Resource, ResourceDigraphEdge

class Knows(ResourceDigraphEdge):
	"""
	Knows represents a connection between two users, but is realized as
	a digraph instead of a forced, edgeless connection that must be
	maintained at both ends.

	This is in a way similar to foaf:knows and will be built as such.
	"""

	# TODO: Programatically enforce 'origin' and 'destination' to be users

	description = models.CharField(max_length=255, null=False, blank=True)

