from datetime import datetime

def auto_apply_editdate(sender, instance, **kwargs):
	"""Automatically apply the editdate whenever a post is edited.
	This is a pre_save callback."""
	print "signal: auto_apply_editdate" # TODO DEBUG
	post = instance
	post.datetime_edited = datetime.today() # TODO: Verify this works

