
from models import User
from sylph.core.node.models import Node
from sylph.utils.uri import hashless
from sylph.utils.transport.Communicator import Communicator
from sylph.utils.data.RdfSerializer import RdfSerializer

# TODO: Eventually this will be controlled via subscription.
def push_profile(node_uri):
	"""Send an updated copy of our profile to a node."""
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

	post = {'distpach': 'user_push'}

	# TODO: Granularized Privacy
	rs = RdfSerializer(user)
	post['data'] = rs.to_rdf()

	comm = Communicator(uri)
	ret = comm.send_post(post)

	if not ret:
		print "User profile push failed." # TODO: Error log

	time = datetime.today()

	node.datetime_last_resolved = time
	node.datetime_last_pushed_to = time
	node.save()

