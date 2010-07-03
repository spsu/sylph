from datetime import datetime

def auto_apply_presave_metadata(sender, instance, **kwargs):
	print "signal: blog.auto_apply_presave_metadata"
	item = instance

	if item.contents:
		item.has_contents = True
	else:
		item.has_contents = False

	if item.summary:
		item.has_sumamry = True
	else:
		item.has_summary = False

