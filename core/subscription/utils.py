# XXX: This is a temporary mechanism
# XXX: This will be replaced when we have granular control (TODO)

from models import Subscription
from datetime import datetime

def __make_default_subscriptions(node):
	"""Makes the default subscriptions.
	They are NOT SAVED, and must be saved by the caller.
	Supply the node or node id."""
	node = __ensure_get_node(node)

	now = datetime.today()

	subs = []

	subs.append(Subscription())
	subs[0].key = 'node'
	subs[0].node = node
	subs[0].push_on_edit = True
	subs[0].datetime_added = now

	subs.append(Subscription())
	subs[1].key = 'user_profile'
	subs[1].node = node
	subs[1].push_on_edit = True
	subs[1].datetime_added = now

	# TODO: Might be some issues with semantics of receiving posts,
	# esp. wrt. posts not for users we follow.
	# (maybe we can just ignore those though...)
	subs.append(Subscription())
	subs[2].key = 'user_profile_posts'
	subs[2].node = node
	subs[2].push_on_create = True
	subs[2].push_on_edit = True
	subs[2].datetime_added = now

	return subs

def create_subscriptions_to(node):
	"""Creates ALL POSSIBLE subscriptions to a node."""
	subscriptions = __make_default_subscriptions(node)

	for subs in subscriptions:
		subs.is_ours = True
		subs.save()

	print "create_subscriptions_to finished" # TODO DEBUG

def create_subscriptions_from(node):
	"""Creates ALL POSSIBLE subscriptions from a node."""
	subscriptions = __make_default_subscriptions(node)

	for subs in subscriptions:
		subs.is_ours = False
		subs.save()

	print "create_subscriptions_from finished" # TODO DEBUG

def delete_subscriptions_to(node):
	"""Deletes ALL POSSIBLE subscriptions to a node."""
	pass

def delete_subscriptions_from(node):
	"""Deletes ALL POSSIBLE subscriptions from a node."""
	pass

def __ensure_get_node(node):
	"""If the node is an ID, look up the node object."""
	if type(node) is int:
		try:
			node = Node.objects.get(pk=node)
		except:
			raise
	return node

