from django.db import models
from sylph.core.resource.models import Resource, ResourceDigraphEdge

from sylph.utils.markdown2 import markdown

from datetime import datetime

class User(Resource):
	"""
	User Resources represent people in the graph.

	We usually store users when we want to keep communications with
	them or follow one or more of their feeds. (Though the system could
	easily store thousands of users for eg. the employees in your
	company, or people in your interest group. Just because a user is
	stored does not mean we are tracking them specifically.)

	Think of this application as your email address list or a phone
	book of the people you have encountered in some way: Another layer
	will build on top of the user system for social networking, etc.

	--

	A user's node is the only authority on how this information should
	be updated/changed locally. When we first encounter a user such as
	by being given a resource they have created, we may	take on metadata
	as provided by the third party that provided us the data. However,
	once a user's node has been contacted, it is the only authority on
	changing data for that user's resource.

	--

	On the topic of the User's "Resource URI", I have some specific
	suggestions:

		1. An OpenID-type system where a page contains <meta> link to
		   the user's current node (such that they can relocate the
		   node or switch providers.) This is the preferred way.

		2. The node URI with some kind of hash appended, eg.
		   http://domain.com/mynode/#user
		   (This is not the preferred approach since the user is stuck
		   with a node they cannot relocate.)
	"""

	# ============= Sylph Metadata ========================

	"""A list of transportable RDF fields."""
	rdf_fields = [
		'username',
		'first_name',
		'middle_name',
		'last_name',
		'title',
		'suffix',
		'bio',
		'node',
	]

	"""A list of fields *not* to transport."""
	rdf_ignore = [
		'datetime_created',
	]

	# ============= Model Fields ==========================

	# Username of the person (The only mandatory field!)
	username = models.CharField(blank=False, null=False, max_length=24)

	# Name of the person (Optional)
	first_name = models.CharField(max_length=30, null=False, blank=True)
	middle_name = models.CharField(max_length=30, null=False, blank=True)
	last_name = models.CharField(max_length=30, null=False, blank=True)

	TITLE_CHOICES = (
		('A', 'Mr.'),
		('B', 'Ms.'),
		('C', 'Mrs.'),
		('D', 'Dr.'),
		('S', 'Sir.'),
		('H', 'Hon.'),
		('R', 'Rev.'),
	)
	title = models.CharField(max_length=1, choices=TITLE_CHOICES,
							 null=False, blank=True)
	suffix = models.CharField(max_length=10, null=False, blank=True)

	bio = models.TextField(blank=True)

	# Cannot send marked-up bio
	bio_markup_cache = models.TextField(blank=True)
	bio_cache_datetime = models.DateTimeField(null=True, blank=True)

	"""FK to the node the user owns."""
	node = models.ForeignKey('node.Node', null=True, blank=True)

	# TODO: Photo the user chooses for their profile
	#photo = models.ForeignKey('images.Photo')

	# TODO: Avatar the user chooses for their posts
	#avatar = models.ForeignKey('images.Avatar')


	# ============= Model-specific methods ================

	def get_name(self):
		"""Get a western-formatted name (if available) or the
		username."""
		# TODO: g11n
		name = "(nameless)"
		if self.username:
			name = self.username
		if self.first_name:
			name = self.first_name
			if self.middle_name:
				name += " " + self.middle_name
			if self.last_name:
				name += " " + self.last_name

		return name

	def get_name_and_title(self):
		"""Get the name and the title."""
		name = self.get_name()
		title = None
		if self.title and self.last_name:
			for t in self.TITLE_CHOICES:
				if self.title == t[0]:
					title = t[1]
					break

		if self.first_name and title:
			name = title + " " + name

		return name

	def bio_with_markup(self):
		"""Get the bio with markup."""
		# TODO: Markup type
		stale = False
		if not self.bio_markup_cache or \
			(self.datetime_edited and \
				self.datetime_edited >= self.bio_cache_datetime):
					stale = True

		if stale:
			markup = markdown(self.bio) # TODO: More markup methods
			self.bio_markup_cache = markup
			self.bio_cache_datetime = datetime.today()
			self.save()

		return self.bio_markup_cache

	def avatar_or_gravatar(self):
		"""Fetches the avatar of the user, or gravatar if no avatar
		is known to exist."""
		pass # TODO

	# ============= Django Methods and Metadata ===========

	class Meta:
		verbose_name = 'user'
		verbose_name_plural = 'users'

	def __unicode__(self):
		return self.username

	def get_absolute_url(self):
		return '/profile/view/%s/' % self.id

class UserEmail(models.Model):
	"""Emails are not resources, this is just a 1:m field for users."""

	# Owner of the email address.
	owner = models.ForeignKey('User')

	# Email account. Uniqueness not enforced, just in case people report false
	# information. 
	email = models.EmailField(unique=False, null=False, blank=False)

	# Let the user briefly describe the email inbox if they choose
	description = models.CharField(max_length=30, blank=True)

	# TODO: organization = models.ForeignKey('Org') (as opposed to User)
	# OR perhaps just use a different table strictly for organizations!

class Knows(ResourceDigraphEdge):
	"""
	Knows represents a connection between two users, but is realized as
	a digraph instead of a forced, edgeless connection that must be
	maintained at both ends.

	This is in a way similar to foaf:knows and will be built as such.
	"""

	# TODO: Programatically enforce 'origin' and 'destination' to be users

	description = models.CharField(max_length=255, null=False, blank=True)

