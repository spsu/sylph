from django.db import models
from django.db.models import signals

class FeedItem(models.Model):
	"""FeedItem is a list of realtime events we wish to show the
	user. This application should be used throughout Sylph."""

	"""The textual description of what occurred."""
	text = models.CharField(max_length=255, blank=False, null=False)

	"""When the event occurred."""
	datetime_added = models.DateTimeField(null=False)

	#"""Broadcast to a specific _channel_, which may display in only
	#a certain place.""" # XXX: TODO
	#channel = models.CharField(max_length=10, blank=True, null=False)

	# TODO: Icon
	# TODO: Class of feed entry
	# TODO: Calculated 'interest level'
