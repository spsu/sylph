from django.conf import settings
from django.db import models
from django.db.models import signals
from django.dispatch import dispatcher

from sylph.core.resource.models import Resource
from sylph.core.resource.models import register_type

from datetime import datetime
import os
import math
from base64 import b64encode

# ============ Nodes ======================================

# TODO: UserNodes and MachineNodes
# TODO: Generic and Advanced permissions

class Node(Resource):
	"""
	Nodes are the machines on the web that can share and communicate
	resources with one another.

	There can be user-owned Nodes, cache Nodes, directory Nodes, and
	so forth.
	"""

	# ============= Sylph Metadata ========================

	# A list of transportable RDF fields
	rdf_fields = [
			'uri',
			'name',
			'description', # TODO: own_description?
			'node_class',
			'protocol_version',
			'software_name',
			'software_version',
			'datetime_edited',
	]

	rdf_ignore = [
			'node_class_guess',
	]

	class_name = 'Node'

	# ============= Model Fields ==========================

	"""A short name for the node."""
	name = models.CharField(max_length=50, null=False, blank=True)

	"""A description for the node (as set by the node owner)."""
	description = models.CharField(max_length=255, null=False, blank=True)

	"""A personal description/note for the node. Never transport this!"""
	own_description = models.CharField(max_length=255, null=False, blank=True)

	# TODO: Media access suburl (is that even necessary?)
	#media_url = models.URLField(max_length=200)

	NODE_CLASS_CHOICES = (
		('unknown', 'Unknown'),
		('sylph', 'Sylph Node'),
		('webpage', 'Webpage'),
		('feed', 'Web feed'),
		('service', 'Web service'),
	)

	"""The type of node."""
	node_class = models.CharField(max_length=10, choices=NODE_CLASS_CHOICES,
									null=False, blank=False)

	"""The type of node the user tells us it is."""
	node_class_guess = models.CharField(max_length=10, choices=NODE_CLASS_CHOICES,
									null=False, blank=True)

	# ======== XXX: There's an API for these ... ====================

	"""Sylph Protocol version"""
	protocol_version = models.CharField(max_length=15, null=False, blank=True)

	"""Client Software name"""
	software_name = models.CharField(max_length=20, null=False, blank=True)

	"""Client Software version"""
	software_version = models.CharField(max_length=15, null=False, blank=True)

	# ======== XXX: There's an API for this ... see methods XXX =====

	"""First time nodes are added, they must be resolved."""
	is_yet_to_resolve = models.BooleanField()

	"""Date the last successful communication with the node occurred on."""
	datetime_last_resolved = models.DateTimeField(null=True)

	"""Date the last failed communication occurred."""
	datetime_last_failed = models.DateTimeField(null=True)

	"""For events originating at the local node"""
	datetime_last_pushed_to = models.DateTimeField(null=True)
	datetime_last_pulled_from = models.DateTimeField(null=True)

	"""For events originating at the remote node"""
	datetime_last_pushed_to_us = models.DateTimeField(null=True)
	datetime_last_pulled_from_us = models.DateTimeField(null=True)

	"""The types of status a node can have""" # XXX: Serious refactor.
	STATUS_TYPE_CHOICES = (
		('U', 'Unknown status'),
		('HOST', 'Host does not resolve.'),
		('SERR', 'Server error.'),
		('EERR', 'Endpoint software error.'),
		('FLOOD', 'Server flooded / bandwidth issue.'),
		('ENDP', 'Not a valid endpoint.'),
		('AVAIL', 'Available / OK.'),
    )
	status = models.CharField(max_length=5, choices=STATUS_TYPE_CHOICES,
								null=False, blank=False, default='U')

	"""
	In the process of mutually adding nodes, we exchange secret keys.
	This isn't for security, but rather to avoid 'doorbell ditching'.
	These keys are uniquely generated for each Node pairing.
	Once PGP is in place, don't use this anymore.

	If a node wants to deal with us, it uses the key we gave them in
	all communications (that update anything).
	"""
	# XXX XXX XXX: This isn't based on actual cryptography...
	key_ours = models.CharField(max_length=100)
	key_ours_confirmed = models.BooleanField(default=False)

	key_theirs = models.CharField(max_length=100)
	key_theirs_confirmed = models.BooleanField(default=False)

	"""In the event keys are being changed, they need to be stored here
	until they can be confirmed by both parties."""
	new_key_ours = models.CharField(max_length=100, null=False, blank=True)
	new_key_theirs = models.CharField(max_length=100, null=False, blank=True)

	DOORBELL_STATUS_CHOICES = (
		('0', 'Ungenerated'),
		# One party has generated a key
		('1', 'One key generated.'),
		# Both parties have generated a key
		('2', 'Both keys generated.'),
		# Both parties have generated a key, and the first party confirmed.
		('3', 'Both keys confirmed!'),
    )
	doorbell_status = models.CharField(max_length=1,
								choices=DOORBELL_STATUS_CHOICES,
								null=False, blank=False, default='0')

	"""TEMP"""
	had_first_lookup_scheduled = models.BooleanField(default=False)

	# ============= Node-specific functionality ===========

	@classmethod
	def generate_key(cls):#, replace=False):
		"""Generate our 'doorbell key' for the other node.
		NOTE: DOES NOT SAVE!"""
		return b64encode(os.urandom(100))[:-2]

	def check_keys(self, our_key, their_key):
		pass

	# ============= Helper methods ========================

	def is_in_class(self, class_list, assumption=True):
		"""Check if the node is in a class type."""
		if self.node_class in class_list:
			return True
		if assumption and self.node_class_guess in class_list:
			return True
		return False

	def get_protocol_version(self):
		return self._get_current_versions()[0]

	def get_software_version(self):
		return self._get_current_versions()[1]

	def get_software_name(self):
		return self._get_current_versions()[2]

	def _get_current_versions(self):
		"""Ensure that the software and protocol versions are always
		in-sync on our deployment."""
		if not self.is_ours():
			return (
				self.protocol_version,
				self.software_version,
				self.software_name
			)

		pver = self.protocol_version
		sver = self.software_version
		name = self.software_name

		stale = False
		if settings.PROTOCOL_VERSION != pver:
			stale = True
		elif settings.SOFTWARE_VERSION != sver:
			stale = True
		elif settings.SOFTWARE_NAME != name:
			stale = True

		if stale:
			# Must update separately of the self instance
			# (It might be changed, but not going to be saved.)
			node = Node.objects.get(pk=settings.OUR_NODE_PK)
			node.protocol_version = pver
			node.software_version = sver
			node.software_name = name
			node.save()

			self.protocol_version = pver
			self.software_version = sver
			self.software_name = name

		return (pver, sver, name)

	# ============= Shortcut methods ======================

	def just_failed(self, save=False):
		"""Set the node state as having just failed to connect."""
		self.datetime_last_failed = datetime.today()
		if save:
			self.save()

	def just_pulled_from(self, save=False):
		"""Set the node state as having pulled from."""
		self.__set_timestamp(save, 'from')

	def just_pushed_to(self, save=False):
		"""Set the node state as having just pushed to."""
		self.__set_timestamp(save, 'to')

	def just_pulled_from_us(self, save=False):
		"""Set the node state as having pulled from us."""
		self.__set_timestamp(save, 'from_us')

	def just_pushed_to_us(self, save=False):
		"""Set the node state as having just pushed to us."""
		self.__set_timestamp(save, 'to_us')

	def __set_timestamp(self, save, term):
		now = datetime.today()
		self.is_yet_to_resolve = False
		self.datetime_last_resolved = now

		if term == 'to':
			self.datetime_last_pushed_to = now
		elif term == 'to_us':
			self.datetime_last_pushed_to_us = now
		elif term == 'from':
			self.datetime_last_pulled_from = now
		elif term == 'from_us':
			self.datetime_last_pulled_from_us = now

		if save:
			self.save()


	# ============= RDF Serilization Helpers ==============

	def alter_transportables(self, transportables):
		"""Overloaded to dynamically replace data with the correct
		server version params."""
		print "Node.AlterTransportables"
		print "Node.AlterTransportables"
		print "Node.AlterTransportables"
		info = self._get_current_versions()
		transportables['protocol_version'] = info[0]
		transportables['software_version'] = info[1]
		transportables['software_name'] = info[2]
		return transportables

	def get_ontology_name(self):
		"""Heuristic to generate the ontology name."""
		# TODO: Temp fix, and does it actually work??
		name = str(type(self))
		name = '/' + name[8:-2] + '#'
		return name.replace('.', '/').replace('/models/', '_')

	def get_rdf_class(self):
		return self.__class__.__name__


	# ============= Template Helpers ======================

	def is_ours(self):
		"""Returns whether this node is ours."""
		return self.pk == settings.OUR_NODE_PK

	def is_not_ours(self):
		"""Returns whether this node is not ours."""
		return self.pk != settings.OUR_NODE_PK

	def status_color(self):
		"""Return a status color for visualization. Temporary."""
		if self.pk == settings.OUR_NODE_PK:
			return 'white'
		if self.node_class == 'unknown':
			return 'gray'
		if self.is_yet_to_resolve:
			return 'red'
		if self.status == 'AVAIL':
			return 'green'
		return 'red'

	def get_status(self):
		if self.pk == settings.OUR_NODE_PK:
			return 'Our node'
		if self.is_yet_to_resolve:
			return 'Unresolved'
		if self.status == 'AVAIL':
			return "Good"
		return "Bad Status"

	def get_class(self):
		"""Get the textual name of the node class"""
		cls = self.node_class_guess
		guess = True
		if self.node_class and self.node_class != 'unknown':
			cls = self.node_class
			guess = False

		ret = 'Unknown'
		for c in self.NODE_CLASS_CHOICES:
			if cls == c[0]:
				ret = c[1]
				break

		if ret == 'Unknown':
			return ret
		if not guess:
			return ret
		return '%s (assumption)' % ret

	# ============= Django Methods and Metadata ===========

	class Meta:
		verbose_name = 'node'
		verbose_name_plural = 'nodes'

	def get_absolute_url(self):
		return "/node/view/%i/" % self.pk

	def protocol_compatibility(self, proto_version):
		"""Compare the protocol version with a compatibility checklist."""
		# TODO: allow lookup against a compatibility checklist
		return proto_version == self.protocol_version

	def __unicode__(self):
		return "node: " + self.uri

# ============ Register Signals ===========================

register_type(Node)

def register_signals():
	"""Register Node signals"""
	import signals as sig_ # To avoid circular imports
	signals.pre_save.connect(sig_.auto_lookup_feed_on_add_blog,
								sender=Node)

register_signals()


