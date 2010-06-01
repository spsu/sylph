from celery.decorators import task
from django.conf import settings

from models import *
from sylph.apps.social.models import User
from sylph.utils.Communicator import Communicator
from sylph.utils.RdfParser import RdfParser

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

	def on_failure(node):
		node.status = 'EERR' # TODO
		node.datetime_last_failed = datetime.today()
		node.save()

	node = None
	try:
		node = Node.objects.get(uri=uri)
	except Node.DoesNotExist:
		# TODO: ERROR LOG FILE
		print "Node does not exist!!!"
		return

	user = None
	try:
		user = User.objects.get(node=node)
	except User.DoesNotExist:
		user = User()

	# Perform communications. 
	comm = Communicator(uri)
	ret = comm.send_post({'dispatch': 'ping'})

	if not ret:
		print "No communication return data!!" # TODO: Error log
		on_failure(node)
		return

	parser = None
	node_data = None
	try:
		parser = RdfParser(ret)
		node_data = parser.extract('Node')
		if not node_data or len(node_data) != 1:
			raise Exception, "Error with data"
		node_data = node_data[0]

	except:
		print "Error parsing RDF" # TODO: Error log
		on_failure(node)
		return

	try:
		user_data = parser.extract('User')
		if not user_data or len(user_data) != 1:
			raise Exception, "Error with data"
		user_data = user_data[0]
	except:
		print "No user data, or error. Ignoring."

	print "Datetime edited:"
	print node_data['datetime_edited']

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
		user.save()

	print "COMM WORKED!!!!"

def query_node_status(uri):
	"""Query a node to see its status."""
	pass

