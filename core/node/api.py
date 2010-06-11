from django.contrib.auth.decorators import login_required
from django.db.models import Model
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from sylph.core.endpoint.exceptions import ProtocolErrorException
from sylph.utils.data.RdfSerializer import RdfSerializer

from sylph.apps.user.models import User
from sylph.core.node.models import Node

import datetime

def ping_response(request):
	"""
	Respond to a 'ping request' from another node.
	This returns node information and (optionally) some user
	information.
	"""
	node = None
	user = None
	try:
		node = Node.objects.get(pk=1)
		user = User.objects.get(pk=1)
	except Model.DoesNotExist:
		raise Exception # XXX: This is a critcal system error!

	rs = RdfSerializer(node)
	rs.add(user) # TODO: Only share minimal info per user's preferences

	return HttpResponse(rs.to_rdf(), mimetype='text/plain')

