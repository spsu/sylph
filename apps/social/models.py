

class User(endpoint.Resource):
	"""
		Users fit the requirement for being a resource:
			* They can be shared with you
			* They can be updated by the owner
			* A stub may exist in our system until we query the owner.

		User resources. Represent people in the graph.

	"""

	# Username of the person (MANDATORY!)
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

	# Photo the user chooses for their profile
	photo = models.ForeignKey('images.Photo')

	# Avatar the user chooses for their posts
	avatar = models.ForeignKey('images.Avatar')



	node = models.ForeignKey('endpoint.Node')

class UserEmail(models.Model):
	"""Emails are not resources, just a 1:m field for users."""

	# Owner of the email address.
	owner = models.ForeignKey('User')

	# TODO: organization = (as opposed to person)
	# OR perhaps just use a different table strictly for organizations.

	# Email account
	email = models.EmailField(unique=True, null=False, blank=False)

	# Let the user describe the email inbox if they choose
	description = models.CharField(max_length=30, blank=True)

