from celery.decorators import task
from django.conf import settings

from models import *
from sylph.apps.social.models import User
from sylph.utils.Communicator import Communicator

from datetime import datetime
import hashlib
import httplib

@task
def do_add_node_lookup(uri):
	"""
	Nodes will get added all the time and in various contexts. 
	This is the task that must run for each of them.

	Query every single added node -- this MUST occur.
	Remember, adding a node doesn't require permission. You can
	navigate to a URI without permission (though you may be blocked)

		if node exists 
			* is on the network
			* is a sylph endpoint
		if uses valid response
			* no server errors
			* no rejection
		protocol version
		software type and version
		node type: user, cache, directory, etc.
		
		The response may provide some additional details:

			* Person (with varying amount of data)
			* etc.

				> Add them
				> Maybe with an additional footnote? (TODO)

		after done, set is_remaining_to_query or whatever = False

		Also, in EVERY outgoing message, tell it what node we are!

	"""

	print "Trying task..." # TODO DEBUG MSG

	node = None
	try:
		node = Node.objects.get(uri=uri)
	except Node.DoesNotExist:
		# TODO: ERROR LOG FILE
		print "Node does not exist!!!"
		return

	comm = Communicator(uri)
	ret = comm.send_post({'dispatch': 'ping'})

	if not ret:
		print "No communication return data!!"
		node.status = 'EERR' # TODO
		node.datetime_last_failed = datetime.today()
		node.save()
		return # TODO: Error

	# Update the node's status
	node.is_yet_to_resolve = False
	node.datetime_last_resolved = datetime.today()
	node.status = 'AVAIL'

	# Data items todo:
	node.protocol_version = 'TODO'
	node.software_name = 'TODO'
	node.software_version = 'TODO'
	node.node_type = 'U' # TODO
	node.name = 'TODO'
	node.description = 'TODO'
	#node.datetime_edited # TODO
	node.save()

	
	print "COMM WORKED!!!!"

def query_node_status(uri):
	"""Query a node to see its status."""
	pass

