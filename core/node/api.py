from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from sylph.core.endpoint.exceptions import ProtocolErrorException
from sylph.utils.Intermediary import Intermediary

from sylph.apps.social.models import User
from sylph.core.node.models import Node

import datetime

def ping_response(request):
	"""
	Respond to a 'ping request' from another node.
	This returns node information and (optionally) some user 
	information.
	"""
	node = None
	try:
		node = Node.objects.get(pk=1)
	except Node.DoesNotExist:
		raise Exception # XXX: This is a critcal system error!

	user = None
	try:
		user = User.objects.get(pk=1)
	except User.DoesNotExist:
		raise Exception # XXX: This is a critcal system error!
	
	im = Intermediary(node)
	im.add(user) # TODO: Only share minimal info per user's preferences
	rdf = im.to_rdf()

	return HttpResponse(rdf, mimetype='text/plain')

