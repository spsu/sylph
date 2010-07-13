from django.conf import settings
from celery.decorators import task
from celery.task.base import PeriodicTask

from models import User
from sylph.core.node.models import Node
from sylph.core.subscription.models import Subscription

from sylph.utils.uri import hashless
#from sylph.utils.transport.Communicator import Communicator
from sylph.utils.data.RdfSerializer import RdfSerializer
from sylph.utils.comms import SylphMessage, send

from datetime import datetime
from datetime import timedelta

@task
def push_profile():
	"""Send the current profile to all subscribers."""
	print "push_profile"
	try:
		subs = Subscription.objects.filter(
								key='user_profile',
								is_ours=False
							)
	except Subscription.DoesNotExist:
		return

	for sub in subs:
		node = sub.node
		if node.is_ours():
			continue # Don't push back to ourself!
		print "Scheduling profile push to: %s" % node.uri
		push_profile_to_node.delay(node.uri)


@task
def push_profile_to_node(node_uri):
	"""Send an updated copy of our profile to a specified node."""
	print "push_profile_to_node %s" % node_uri

	node_uri = hashless(node_uri)
	node = None
	user = None
	try:
		user = User.objects.get(pk=settings.OUR_USER_PK)
		node = Node.objects.get(uri=node_uri)
	except User.DoesNotExist:
		raise Exception, "The main user MUST exist!"
	except Node.DoesNotExist:
		raise Exception, "The node requested does not exist."

	# TODO: Granularized Privacy

	message = SylphMessage(node_uri)
	message.set_post('dispatch', 'user_push')
	message.add(user)
	response = send(message)

	if not response.has_errors():
		node.just_failed(save=True)
		print "User profile push failed." # TODO: Error log
		return

	node.just_pushed_to(save=True)

@task
def pull_profile_from_node(node_id):
	"""Pull the user profile from the given node id
	Only update the user if data has changed."""
	print "pull_profile_from_node %d" % node_id

	save = False # Flag to save user
	node = None
	try:
		node = Node.objects.get(pk=node_id)
	except Node.DoesNotExist:
		# TODO: ERROR LOG FILE
		print "Node does not exist!!!"
		return

	user = None
	try:
		user = User.objects.get(node=node)
	except User.DoesNotExist:
		print "We don't have a user for the node..."
		user = User() # We may not yet have a user for the node (rare)
		save = True

	# Perform communications
	message = SylphMessage(node.uri)
	message.set_post('dispatch', 'user_pull')
	response = send(message)

	if response.has_errors():
		print "No communication return data!!" # TODO: Error log
		node.just_failed(save=True)
		return

	try:
		user_data = response.extract('User')
		if not user_data or len(user_data) != 1:
			raise Exception, "Error with data"
		user_data = user_data[0]
	except Exception: 
		print "No user data, or error. Ignoring."
		node.just_failed(save=True)
		return

	node.just_pulled_from(save=True)

	for k, v in user_data.iteritems():
		chk = getattr(user, k)
		if v == chk:
			continue
		if k == 'node':
			if v == node.pk:
				continue
			# XXX: The following could be used to hijack other users
			user.node = node # TODO: This isn't correct.
			save = True
			continue
		save = True
		setattr(user, k, v) # TODO: Might not work for 'uri' or 'node'

	if save:
		user.save()

"""
#=================
# PERIODIC TASKS
#=================
"""

# ============ Periodic Pull Profile ======================

class PeriodicPullProfile(PeriodicTask):
	"""Periodically pull profiles."""

	run_every = timedelta(seconds=10)
	#run_every = timedelta(hours=2)

	def run(self, **kwargs):
		#print "PeriodicPullProfile" # TODO: Debug
		logger = self.get_logger(**kwargs)
		logger.info("Pulling profiles")

		try:
			subs = Subscription.objects.filter(
									key='user_profile',
									is_ours=True
								)
		except Subscription.DoesNotExist:
			return

		# TODO: Respond to server overload
		for sub in subs:
			node = sub.node
			print "Scheduling profile pull from node %d" % node.pk
			pull_profile_from_node.delay(node.pk)


