from django.db import models
from sylph.core.endpoint.models import Resource

class User(Resource):
	"""
	User resources represent people in the graph. They support being
	largely incomplete as data is missing by default. 

	Users fit the requirement for being a resource:
		* They can be shared with you
		* They can be updated by the owner
		* A stub may exist in our system until we query the owner.
	"""

	# Username of the person (The only mandatory field!)
	username = models.CharField(blank=False, null=False, max_length=30)

	# Name of the person (Optional)
	first_name = models.CharField(max_length=30, null=False, blank=True)
	middle_name = models.CharField(max_length=30, null=False, blank=True)
	last_name = models.CharField(max_length=30, null=False, blank=True)

	TITLE_CHOICES = (
		('A', 'Mr.'),
		('B', 'Ms.'),
		('C', 'Mrs.'),
		('D', 'Dr.'),
		('S', 'Sir'),
		('H', 'Hon.'),
	)
	title = models.CharField(max_length=1, choices=TITLE_CHOICES)
	suffix = models.CharField(max_length=10, null=False, blank=True)

	# TODO: Photo the user chooses for their profile
	#photo = models.ForeignKey('images.Photo')

	# TODO: Avatar the user chooses for their posts
	#avatar = models.ForeignKey('images.Avatar')

	# TODO: Node the user owns
	#node = models.ForeignKey('endpoint.Node')

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


