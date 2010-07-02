from models import *

def auto_lookup_feed_on_add_blog(sender, instance, **kwargs):
	"""When a subscription is added for the first time, schedule an
	immediate lookup. It's boring to wait!!"""
	print "signal: auto_lookup_feed_on_add_blog"

	# TODO/XXX: I'm assuming these are bootstrapped
	node = instance

	# Can't reasonably be guaranteed this data is set yet.
	# Depends on the order the callbacks were dispathed.
	if node.resource_type in ['Node', 'SylphNode', 'WebServiceNode']:
		return

	# This field is only for this signal...
	try:
		if node.had_first_lookup_scheduled:
			return
	except:
		return

	node.had_first_lookup_scheduled = True

	# We need the primary key to schedule 
	# The above code should avoid infinite loops
	if not node.pk:
		node.save()

	from sylph.apps.blog.tasks import get_feed
	get_feed.delay(node.pk)

