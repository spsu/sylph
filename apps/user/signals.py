
#from models import User
import tasks

def schedule_notify_profile_change(sender, instance, **kwargs):
	"""Signal handler schedule the notification of other nodes
	of our profile change/update.
	Only runs for changes to our user model."""
	user = instance
	if user.is_owner():
		# Push profile updates...
		tasks.push_profile.delay()

