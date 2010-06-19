
#from models import User
import tasks
from datetime import datetime

def schedule_notify_profile_change(sender, instance, **kwargs):
	"""Signal handler schedule the notification of other nodes
	of our profile change/update.
	Only runs for changes to our user model."""
	user = instance
	if user.is_owner():
		# Push profile updates...
		tasks.push_profile.delay()

def auto_apply_editdate(sender, instance, **kwargs):
	"""Automatically apply the editdate whenever our profile is saved.
	This is a pre_save callback."""
	print "signal: auto_apply_editdate" # TODO DEBUG
	user = instance
	if not user.is_owner():
		return
	user.datetime_edited = datetime.today() # TODO: Verify this works

