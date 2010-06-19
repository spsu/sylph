from celery.decorators import task

from models import User
from sylph.core.node.models import Node
from sylph.utils.uri import hashless
from sylph.utils.transport.Communicator import Communicator
from sylph.utils.data.RdfSerializer import RdfSerializer

from datetime import datetime

@task
def push_profile():
	"""Send the current profile to all subscribers
	Right now, that means all nodes in the system."""
	# TODO: Subscription system
	try:
		nodes = Node.objects.exclude(pk=1)
	except:
		raise Exception, "Could not get nodes."

	print "push profile"

	# TODO: Subscription system instead
	# Schedule delivery to each node.
	for node in nodes:
		push_profile_to_node.delay(node.uri)


# TODO: Eventually this will be controlled via subscription.
@task
def push_profile_to_node(node_uri):
	"""Send an updated copy of our profile to a specified node."""

	print "push_profile_to_node %s" % node_uri

	node_uri = hashless(node_uri)
	node = None
	user = None
	try:
		user = User.objects.get(pk=1)
		node = Node.objects.get(uri=node_uri)
	except User.DoesNotExist:
		raise Exception, "The main user MUST exist!"
	except Node.DoesNotExist:
		raise Exception, "The node requested does not exist."

	post = {'dispatch': 'user_push'}

	# TODO: Granularized Privacy
	rs = RdfSerializer(user)
	post['data'] = rs.to_rdf()

	comm = Communicator(node_uri)
	ret = comm.send_post(post)

	if not ret:
		print "User profile push failed." # TODO: Error log

	time = datetime.today()

	node.datetime_last_resolved = time
	node.datetime_last_pushed_to = time
	node.save()

