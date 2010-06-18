from django.contrib.auth.decorators import login_required
from django.db.models import Model
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from sylph.core.endpoint.exceptions import ProtocolErrorException
from sylph.utils.data.RdfSerializer import RdfSerializer

from sylph.apps.user.models import User
from sylph.core.node.models import Node

from sylph.utils.uri import hashless

import datetime

# ============ Ping Response ==============================

def ping_response(request):
	"""
	Respond to a 'ping request' from another node.
	This returns node information and (optionally) some user
	information.
	"""
	node = None
	user = None
	try:
		node = Node.objects.get(pk=2)
		user = User.objects.get(pk=1)
	except Model.DoesNotExist:
		raise Exception # XXX: This is a critcal system error!

	rs = RdfSerializer(node)
	rs.add(user) # TODO: Only share minimal info per user's preferences

	return HttpResponse(rs.to_rdf(), mimetype='text/plain')


# ============ Add Response ===============================

def add(request):
	"""
	The other node is asking that we mutually form a connection.
	This usually means that both endpoints will add each other.

		1. NodeA	(add)-->	NodeB
		2. NodeA	<---(add)	NodeB

	(Note: this could be maliciously taken advantage of.) FIXME.

		POSTDATA:
			* node = uri
			* key_ours = ...
			* key_yours = ...
	"""
	if not request.method != 'POST':
		raise Exception, "Not a post..."

	p = request.POST

	uri = hashless(p['uri'])
	key_ours = p['key_theirs'] if 'key_theirs' in p else None
	key_theirs = p['key_yours'] if 'key_yours' in p else None

	# Lookup or create node.
	# TODO: For now assume it exists. Deal with spam later.
	node = None
	try:
		node = Node.objects.get(uri=uri)
	except Node.DoesNotExist:
		node = Node(uri=uri)
		node.datetime_added = datetime.today()
		node.is_yet_to_resolve = True
		node.save()
		#tasks.do_add_node_lookup.delay(form.cleaned_data['uri'])

	state = node.doorbell_status

	if state not in ['0', '1', '2', '3']:
		raise Exception, "Invalid state."

	# They're asking to add us first
	if state == '0':
		node.key_theirs = key_theirs
		node.generate_key()
		node.doorbell_status = '2'
		node.save()
		return HttpResponse('ACK') # TODO: Acknowledge

	# They're responding back to our request to add them.
	if state == '1':
		if node.key_ours != key_ours:
			raise Exception, "Key does not match."
		node.key_theirs = key_theirs
		node.doorbell_status = 3
		node.is_yet_to_resolve = False
		node.save()
		return HttpResponse('ACK') # TODO: Acknowledge

	# Both keys have been generated, but perhaps they're asking to
	# change them.

	# TODO
	pass

