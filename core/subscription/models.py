from django.db import models

class Subscription(models.Model):
	"""
	Subscriptions represent the interaction our node has with other
	nodes. They are used to fine-control the type, rate, etc. that
	specific types of data are exchanged.

	In a way, you can think of these as "feed subcriptions", but for
	Resources instead of RSS/Atom.
	"""

	"""The node that this subscription involves."""
	node = models.ForeignKey('Node')

	"""Represents whether this is our subscription (that we're
	requesting from the remote node), or is another node's (that they
	are requesting from us)."""
	is_ours = models.BooleanField()

	"""The time the subscription was created locally."""
	datetime_created = models.DateTimeField(blank=False, null=False)

	"""The last time the subscription parameters were edited (by us
	or by the remote node)."""
	datetime_edited = models.DateTimeField(blank=True, null=False)

	"""The last time a communication was instigated remotely."""
	datetime_last_inbound = models.DateTimeField(blank=True, null=False)

	"""The last time a communication was instigated locally."""
	datetime_last_outbound = models.DateTimeField(blank=True, null=False)

	"""The last time an error in communication occurred."""
	datetime_last_error = models.DateTimeField(blank=True, null=False)

	"""The number of consecutive errors if the last communication
	resulted in an error. (This can be used to find problems in
	communication.)"""
	consecutive_error_count = models.IntegerField(blank=True, null=False)

