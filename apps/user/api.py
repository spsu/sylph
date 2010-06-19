from sylph.apps.user.models import User
from sylph.core.node.models import Node
from sylph.utils.uri import hashless
from sylph.utils.data.RdfSerializer import RdfSerializer
from sylph.utils.data.RdfParser import RdfParser

# ============ Get owner's profile ========================

def get_profile(request):
	"""
	Get up-to-date information on the owner of this node.
	In the future this will respect privacy issues. There may also be
	more data than the simple profile serialized into this.
	"""
	try:
		user = User.objects.get(id=1)
	except User.DoesNotExist:
		raise Exception, "Critical error: no user!" # XXX: Core system error!

	# XXX/TODO/FIXME: Privacy issues!!

	# TODO: Email, etc.

	rs = RdfSerializer(user)
	return HttpResponse(rs.to_rdf(), mimetype='text/plain')


def update_profile(request):
	"""
	Handle a profile that has been sent to us.
	"""
	p = request.POST

	try:
		ps = RdfParser(p['data'])
		udata = ps.extract('User')[0]
	except:
		raise Exception, "Improper payload."

	uri = udata['uri']
	node_uri = udata['node']

	del udata['uri']
	del udata['node']

	try:
		user = User.objects.get(uri=uri)
	except User.DoesNotExist:
		user = User(uri=uri)

	try:
		node = Node.objects.get(uri=node_uri)
	except Node.DoesNotExist:
		node = Node(uri=node_uri)

	# TODO: There's no security in this...
	for k, v in udata.iteritems():
		setattr(user, k, v)

	user.node = node
	user.save()


# ================= SELDOM USED ===========================

# ============ Get info on an arbitrary user ==============

def get(request):
	"""
	Get information on a user given their user resource URI.
	This isn't authoratative, since we're not looking up the
	originating source.
	"""
	if 'uri' not in request.POST:
		raise Exception, "No URI in post."

	uri = hashless(request.POST['uri'])
	try:
		user = User.objects.get(uri=uri)
	except User.DoesNotExist:
		raise Exception, "User does not exist."

	# XXX/TODO/FIXME: Privacy issues!!
	rs = RdfSerializer(user)
	return HttpResponse(rs.to_rdf(), mimetype='text/plain')


# ============ Get info on an arbitrary user ==============

def get_by_node(request):
	"""
	Get information on a user given their node resource URI.
	See: get(resource).
	"""
	if 'uri' not in request.POST:
		raise Exception, "No URI in post."

	uri = hashless(request.POST['uri'])

	try:
		user = User.objects.get(node__uri=uri)
	except User.DoesNotExist:
		raise Exception, "User does not exist."

	# XXX/TODO/FIXME: Privacy issues!!
	rs = RdfSerializer(user)
	return HttpResponse(rs.to_rdf(), mimetype='text/plain')

