from celery.decorators import task
from celery.task.base import PeriodicTask

from django.conf import settings

from models import *
from sylph.apps.user.models import User
from sylph.utils.transport.Communicator import Communicator
from sylph.utils.transport.Request import Request
from sylph.utils.data.RdfParser import RdfParser
from sylph.utils.uri import hashless

from sylph.core.subscription.utils import create_subscriptions_to
from sylph.core.subscription.utils import create_subscriptions_from

from datetime import datetime, timedelta

# ============ Add Node (Mutual) ==========================

@task
def add_node(uri):
	"""
	Add Node
	Resolves the remote node and notifies it that we'll be adding
	them to our list of tracked nodes. (They are free to add us.)
	"""
	uri = hashless(uri)

	node = None
	try:
		node = Node.objects.get(uri=uri)
	except Node.DoesNotExist:
		# XXX: Technically, it should already be in the DB
		node = Node(uri=uri)
		node.datetime_added = datetime.today()
		node.is_yet_to_resolve = True
		node.status = 'U'
		node.save()

	# Now let's exchange doorbell key info...
	state = node.doorbell_state
	if not node.dispatch_key_ours:
		node.generate_key()
		node.save()

	if state not in ['0', '1', '2', '3']:
		raise Exception, "State is non-normative" # XXX ERROR LOG

	post = {'dispatch': 'node_add'}
	new_state = None

	# We're contacting them first.
	if state == '0':
		post['key_ours'] = node.dispatch_key_ours
		new_state = '1'

	# We're responding to their request.
	if state == '1':
		post['key_ours'] = node.display_key_ours
		post['key_yours'] = node.display_key_theirs
		new_state = '3'

	comm = Communicator(node.uri)
	ret = comm.send_post(post)

	time = datetime.today()

	if not ret or ret == 'NACK':
		print "No communication return data!!" # TODO: Error log
		node.status = 'EERR' # TODO
		node.datetime_last_failed = time
		node.save()
		return

	node.is_yet_to_resolve = False
	node.datetime_last_resolved = time
	node.datetime_last_pulled_from = time
	node.doorbell_state = new_state
	node.save()

	# Unknown other state...
	raise Exception, "Unknown state."



# ============ Initial Node Adding ========================

# TODO: DEPRECATED
@task
def do_add_node_lookup(uri):
	"""
	Nodes will get added all the time and in various contexts.
	This is the task that must run for each of them.

	Query every single added node -- this MUST occur.
	Remember, adding a node doesn't require permission. You can
	navigate to a URI without permission (though you may be blocked)

	The response may provide some additional details:

		* Person (with varying amount of data)
		* etc.

			> Add them
			> Maybe with an additional footnote? (TODO)

	after done, set is_remaining_to_query or whatever = False

	Pinging a node does not require us to give identity unless the
	remote node requests it.
	"""

	def on_failure(node):
		node.status = 'EERR' # TODO
		node.datetime_last_failed = datetime.today()
		node.save()

	node = None
	try:
		node = Node.objects.get(uri=uri)
	except Node.DoesNotExist:
		# TODO: ERROR LOG FILE
		print "cannot do_add_node_lookup: Node does not exist!!!"
		return

	if node.node_type == 'Z':
		print "cannot do_add_node_lookup: non-sylph nodes (type Z)"
		return

	user = None
	try:
		user = User.objects.get(node=node)
	except User.DoesNotExist:
		user = User()

	# Perform communications
	comm = Communicator(uri)
	ret = comm.send_post({'dispatch': 'ping'})

	if not ret:
		print "No communication return data!!" # TODO: Error log
		on_failure(node)
		return

	parser = None
	node_data = None

	try:
		node_data = ret.extract('Node')[0]
	except:
		print "Error parsing RDF" # TODO: Error log
		on_failure(node)
		return

	user_data = None
	try:
		user_data = ret.extract('User')[0]
	except:
		print "1. No user data, or error. Ignoring."

	# Update the node's status
	node.is_yet_to_resolve = False
	node.datetime_last_resolved = datetime.today()
	node.status = 'AVAIL'
	node.protocol_version = node_data['protocol_version']
	node.software_name = node_data['software_name']
	node.software_version = node_data['software_version']
	node.node_type = 'U' # TODO
	node.name = node_data['name']
	node.description = node_data['description']
	#node.datetime_edited = node_data['datetime_edited'] # TODO
	node.save()

	# Update the user's status, if we have user data.
	if user_data:
		user.username = user_data['username']
		user.first_name = user_data['first_name']
		user.middle_name = user_data['middle_name']
		user.last_name = user_data['last_name']
		user.bio = user_data['bio']
		user.title = user_data['title']
		user.suffix = user_data['suffix']
		#user.datetime_created = user_data['datetime_created']
		#user.datetime_edited = user_data['datetime_edited']
		user.node = node
		user.save()

	# Now have the node add us
	comm = Communicator(uri)
	post = {'dispatch': 'node_ask_to_add'}
	post['uri'] = settings.FULL_ENDPOINT_URI
	ret = comm.send_post(post)

	print "CREATING SUBSCRIPTIONS:"
	create_subscriptions_to(node)
	create_subscriptions_from(node)

def query_node_status(uri):
	"""Query a node to see its status."""
	pass

# ============ Ping Already Resolved Nodes ================

@task
def ping_node(id):
	"""Ping a node that has already been added and succesfully resolved
	in the past. This keeps info up to date."""

	#def on_failure(node):
	#	node.status = 'EERR' # TODO
	#	node.datetime_last_failed = datetime.today()
	#	node.save()

	node = None
	try:
		node = Node.objects.get(pk=id)
	except Node.DoesNotExist:
		# TODO: ERROR LOG FILE
		print "Node does not exist!!!"
		return

	# XXX: Temporarily disabled
	#user = None
	#try:
	#	user = User.objects.get(node=node)
	#except User.DoesNotExist:
	#	user = User()

	# Perform communications. 
	comm = Communicator(node.uri)
	ret = comm.send_post({'dispatch': 'ping'})

	if not ret:
		print "No communication return data!!" # TODO: Error log
		node.just_failed(save=True)
		return

	node_data = None
	try:
		node_data = ret.extract('Node')
		if not node_data or len(node_data) != 1:
			raise Exception, "Error with data"
		node_data = node_data[0]

	except:
		print "Error parsing RDF" # TODO: Error log
		node.just_failed(save=True)
		return

	# XXX: Temporarily disabled
	#try:
	#	user_data = ret.extract('User')
	#	if not user_data or len(user_data) != 1:
	#		raise Exception, "Error with data"
	#	user_data = user_data[0]
	#except:
	#	pass

	# Update the node's status
	node.datetime_last_resolved = datetime.today()
	node.status = 'AVAIL'
	node.protocol_version = node_data['protocol_version']
	node.software_name = node_data['software_name']
	node.software_version = node_data['software_version']
	node.node_type = 'U' # TODO: Codes are messy
	node.name = node_data['name']
	node.description = node_data['description']
	#node.datetime_edited = node_data['datetime_edited'] # TODO
	node.save()

	node.just_pulled_from(save=True)

	# XXX: Temporarily disabled
	# Update the user's status, if we have user data.
	#if user_data:
	#	user.username = user_data['username']
	#	user.first_name = user_data['first_name']
	#	user.middle_name = user_data['middle_name']
	#	user.last_name = user_data['last_name']
	#	user.bio = user_data['bio']
	#	user.title = user_data['title']
	#	user.suffix = user_data['suffix']
	#	#user.datetime_created = user_data['datetime_created']
	#	#user.datetime_edited = user_data['datetime_edited']
	#	user.save()


# ============ Retry Failed Nodes =========================

class RetryFailedNodesTask(PeriodicTask):
	"""Retry Nodes that failed to add."""

	run_every = timedelta(seconds=20)
	#run_every = timedelta(minutes=2)

	def run(self, **kwargs):
		logger = self.get_logger(**kwargs)
		logger.info("Retry Nodes that failed to add")

		nodes = None
		try:
			nodes = Node.objects.filter(is_yet_to_resolve=True) \
								.exclude(node_type='Z') # non-sylph
		except:
			return

		# TODO: Respond to server overload
		for node in nodes:
			print "Scheduling node %d" % node.pk
			do_add_node_lookup.delay(node.uri)


# ============ Keep Resolving Added Nodes =================

class KeepResolvingAddedNodes(PeriodicTask):
	"""Re-resolve nodes that have been successfully added in the past"""

	run_every = timedelta(seconds=10)
	#run_every = timedelta(hours=2)

	def run(self, **kwargs):
		print "KeepResolvingAddedNodes" # TODO: Debug
		logger = self.get_logger(**kwargs)
		logger.info("Re-resolve existing nodes")

		nodes = None
		nodes = Node.objects.filter(is_yet_to_resolve=False) \
							.exclude(node_type='Z') \
							.exclude(pk=settings.OUR_NODE_PK)


		# TODO: Respond to server overload
		for node in nodes:
			print "Scheduling node %d" % node.pk
			ping_node.delay(node.pk)


