from datetime import datetime

def auto_apply_editdate(sender, instance, **kwargs):
	"""Automatically apply the editdate whenever a post is edited.
	This is a pre_save callback."""
	print "signal: auto_apply_editdate" # TODO DEBUG
	post = instance
	post.datetime_edited = datetime.today() # TODO: Verify this works

def auto_apply_presave_metadata(sender, instance, **kwargs):
	print "signal: auto_apply_presave_metadata"
	post = instance
	if post.contents:
		post.has_contents = True
	else:
		post.has_contents = False

