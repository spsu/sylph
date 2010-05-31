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
	node = None
	try:
		node = Node.objects.get(uri=uri)
	except Node.DoesNotExist:
		# TODO: ERROR LOG FILE
		return

	comm = Communicator(uri)

	ret = comm.send_post({'todo':0})

	print ret


def query_node_status(uri):
	"""Query a node to see its status."""
	pass

