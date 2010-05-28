from django.contrib.auth.models import User

# TODO: Semantics of this class are a bit weird.
class UserAccount(object):
	"""Wrapper class for the singular user account allowed in the sylph 
	software. Only one user account can exist. One person per node for now."""

	# Singular user account for the system. 
	ACCOUNT = None

	# If the database has been checked for an account
	__CHECKED = False 

	def __init__(self):
		"""Constructor for instances."""
		UserAccount.__getUserIfExist()

	@classmethod
	def exists(cls):
		"""Whether a user account exists."""
		cls.__getUserIfExist()

		if cls.ACCOUNT:
			return True
		return False

	@classmethod
	def create(cls, username, password):
		"""Create the initial user account. This can only be done once."""
		if cls.exists():
			return False

		user = User.objects.create_user(username, email, 'noemail@noemail.com')
		user.is_staff = True
		user.save()

		cls.ACCOUNT = user
		return True

	@classmethod
	def __getUserIfExist(cls):
		"""Helper method to get the user account if it exists."""
		if cls.__CHECKED:
			return

		users = User.objects.all()

		if len(users) > 1:
			raise Exception, "Too many sylph accounts exist!"

		cls.__CHECKED = True

		if len(users) == 1:
			cls.ACCOUNT = users[0]

		


