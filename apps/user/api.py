from sylph.apps.user.models import User
from sylph.utils.uri import hashless
from sylph.utils.data.RdfSerializer import RdfSerializer

def update(request):
	"""
	Get up-to-date information on the owner of the node.
	In the future this will respect privacy issues. There may also be
	more data than the simple profile serialized into this.
	"""
	try:
		user = User.objects.get(id=1)
	except User.DoesNotExist:
		raise Exception, "Critical error: no user!" # XXX: Core system error!

	# XXX/TODO/FIXME: Privacy issues!!
	rs = RdfSerializer(user)
	return HttpResponse(rs.to_rdf(), mimetype='text/plain')


def get(request):
	"""
	Get information on a user given their user resource URI.
	This isn't authoratative, since we're not looking up the
	originating source.
	"""
	if 'uri' not in request.POST:
		raise Exception, "No URI in post.'

	uri = hashless(request.POST['uri'])
	try:
		user = User.objects.get(uri=uri)
	except User.DoesNotExist:
		raise Exception, "User does not exist."

	# XXX/TODO/FIXME: Privacy issues!!
	rs = RdfSerializer(user)
	return HttpResponse(rs.to_rdf(), mimetype='text/plain')


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

