from django.db import models
from django.db.models import signals
from django.dispatch import dispatcher
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
	# TODO: Rename 'alias' for less of a dull/traditional feel
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

	def is_owner(self):
		"""Return whether the user is the owner of *this* node."""
		return (self.pk == 1)

	def set_name(self, name):
		"""A heuristic for setting all of the name components based on
		a single input string. NOTE: DOES NOT CALL SAVE()!"""
		if not name or type(name) not in [str, unicode]:
			raise Exception, "Invalid input"

		parts = name.split()
		ln = len(parts)

		if not parts:
			return

		self.first_name = parts[0]
		self.middle_name = ''
		self.last_name = ''

		if ln == 2:
			self.last_name = parts[1]
		elif ln == 3:
			self.middle_name = parts[1]
			self.last_name = parts[2]


	def get_name(self):
		"""Get a western-formatted name (if available)."""
		# TODO: g11n
		name = "(nameless)"
		if self.first_name:
			name = self.first_name
			if self.middle_name:
				name += " " + self.middle_name
			if self.last_name:
				name += " " + self.last_name

		return name

	def get_name_or_username(self):
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

	def get_username(self):
		"""Get the username (if available)."""
		name = "(no username)"
		if self.username:
			name = self.username
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

		if not self.bio:
			return ''

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
		return '/user/view/%s/' % self.id


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


# ============ Signal registration ========================

"""Register signals."""
def register_signals():
	import signals as sig_ # To avoid circular imports
	signals.post_save.connect(sig_.schedule_notify_profile_change,
								sender=User)

	signals.pre_save.connect(sig_.auto_apply_editdate,
								sender=User)

register_signals()

